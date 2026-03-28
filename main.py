import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# ============ CONSTANTS & CONFIGURATION ============
LI_TOKEN = os.getenv("LINKEDIN_TOKEN")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "sk-MYAPIKEY")
STABILITY_API_URL = "https://api.stability.ai/v2beta/stable-image/generate/ultra"

if not LI_TOKEN:
    print("⚠️  WARNING: LINKEDIN_TOKEN not found in .env")

# ============ CONSTANTS ============
DEFAULT_POST_TEXT = "Check out our content! #LinkedInPost"
DEFAULT_IMAGE_PROMPT = "Professional business photo, high quality, 8k"

def get_linkedin_person_id():
    """
    Fetches your unique LinkedIn Member ID using the OpenID userinfo endpoint.
    
    Returns:
        str: LinkedIn user ID or None if failed
    """
    if not LI_TOKEN:
        print("❌ Error: LINKEDIN_TOKEN not configured. Add it to .env file.")
        return None
    
    try:
        headers = {'Authorization': f'Bearer {LI_TOKEN}'}
        response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers, timeout=10)
        
        if response.status_code == 200:
            person_id = response.json().get('sub')
            if person_id:
                print(f"✅ LinkedIn ID verified: {person_id}")
                return person_id
            else:
                print("❌ Failed to get Person ID from response")
                return None
        elif response.status_code == 401:
            print("❌ Authentication failed: Invalid or expired LinkedIn token")
            return None
        else:
            print(f"❌ LinkedIn API Error {response.status_code}: {response.text}")
            return None
    
    except requests.exceptions.Timeout:
        print("❌ Request timed out. LinkedIn API is not responding.")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None


# ============ FUNCTIONS ============

def generate_ai_image(prompt, output_path="generated_image.webp"):
    """
    Generates ultra-realistic images using Stability AI's Ultra model.
    
    Args:
        prompt (str): Image description
        output_path (str): File path to save the image
    
    Returns:
        str: Path to generated image or None if failed
    """
    print(f"\n📸 Generating image with Stability AI Ultra...")
    print(f"📝 Prompt: {prompt}")
    print(f"⏳ Processing...\n")

    try:
        response = requests.post(
            STABILITY_API_URL,
            headers={
                "authorization": f"Bearer {STABILITY_API_KEY}",
                "accept": "image/*"
            },
            files={"none": ''},
            data={"prompt": prompt, "output_format": "webp"},
            timeout=60
        )

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)

            print(f"Image generated successfully!")
            print(f"Saved: {output_path}")
            print(f" Format: WEBP (1024x1024px)\n")
            return output_path
        else:
            try:
                error_msg = response.json()
            except:
                error_msg = response.text
            print(f"API Error {response.status_code}: {error_msg}\n")
            return None

    except requests.exceptions.Timeout:
        print(f"Request timed out. Please try again.\n")
        return None
    except Exception as e:
        print(f" Error: {str(e)}\n")
        return None

def upload_image_to_linkedin(image_path):
    """
    Uploads an image to LinkedIn and returns the media asset URN.
    
    Args:
        image_path (str): Path to the image file to upload
    
    Returns:
        str: Media asset URN or None if failed
    """
    # Validate image exists
    if not image_path or not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return None
    
    # Check file size (LinkedIn max is ~10MB)
    file_size = os.path.getsize(image_path)
    if file_size > 10 * 1024 * 1024:
        print(f"Image too large: {file_size / 1024 / 1024:.1f}MB (max 10MB)")
        return None
    
    person_id = get_linkedin_person_id()
    if not person_id:
        print("Cannot upload: Unable to authenticate with LinkedIn")
        return None
    
    try:
        headers = {
            'Authorization': f'Bearer {LI_TOKEN}',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        print("\nUploading image to LinkedIn...")
        
        # Step 1: Register the upload
        register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        
        register_data = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": f"urn:li:person:{person_id}",
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }
        
        register_response = requests.post(register_url, headers=headers, json=register_data, timeout=15)
        if register_response.status_code != 200:
            print(f"Failed to register upload: {register_response.status_code}")
            print(f"   Response: {register_response.text}")
            return None
        
        # Extract upload URL and asset URN
        try:
            response_json = register_response.json()
            upload_url = response_json['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            asset_urn = response_json['value']['asset']
        except (KeyError, TypeError) as e:
            print(f"Unexpected response format: {str(e)}")
            return None
        
        # Step 2: Upload the image
        print("   Uploading...")
        with open(image_path, 'rb') as f:
            upload_response = requests.put(upload_url, data=f, headers={'Authorization': f'Bearer {LI_TOKEN}'}, timeout=30)
        
        if upload_response.status_code != 201:
            print(f"Failed to upload image: {upload_response.status_code}")
            print(f"   Response: {upload_response.text}")
            return None
        
        print(f"✅ Image uploaded successfully!")
        return asset_urn
    
    except requests.exceptions.Timeout:
        print("❌ Upload request timed out. Please try again.")
        return None
    except Exception as e:
        print(f"Upload error: {str(e)}")
        return None

def post_to_linkedin(text, image_path=None):
    """
    Sends text (and optionally an image) to your LinkedIn Feed.
    
    Args:
        text (str): Post content text
        image_path (str, optional): Path to image file to attach
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not text or not text.strip():
        print("Error: Post text cannot be empty")
        return False
    
    person_id = get_linkedin_person_id()
    if not person_id:
        return False

    # Upload image if provided
    media_asset = None
    if image_path:
        media_asset = upload_image_to_linkedin(image_path)
        if not media_asset:
            print("Continuing without image...")

    try:
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            'Authorization': f'Bearer {LI_TOKEN}',
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json'
        }
        
        # Build post data
        share_content = {
            "shareCommentary": {"text": text},
        }
        
        if media_asset:
            share_content["shareMediaCategory"] = "IMAGE"
            share_content["media"] = [{"status": "READY", "media": media_asset}]
        else:
            share_content["shareMediaCategory"] = "NONE"
        
        post_data = {
            "author": f"urn:li:person:{person_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": share_content
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        
        print("\n🚀 Publishing to LinkedIn...")
        response = requests.post(url, headers=headers, json=post_data, timeout=15)
        
        if response.status_code == 201:
            print("✅ SUCCESS! Your post is now live on LinkedIn!")
            return True
        elif response.status_code == 401:
            print("❌ Authentication failed: Check your LinkedIn token")
            return False
        elif response.status_code == 403:
            print("❌ Permission denied: Account may not have posting permissions")
            return False
        else:
            print(f"❌ LinkedIn Post Failed: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"   Error: {error_detail}")
            except:
                print(f"   Response: {response.text}")
            return False
    
    except requests.exceptions.Timeout:
        print(" Request timed out. Please try again.")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

# --- MAIN LOGIC ---
if __name__ == "__main__":
    print("🤖 LinkedIn AI Content & Image Poster")
    print("=" * 60)
    print()
    
    # Verify configuration
    if not LI_TOKEN:
        print(" Fatal Error: LINKEDIN_TOKEN not configured.")
        print("   Please add LINKEDIN_TOKEN to your .env file")
        exit(1)
    
    if not STABILITY_API_KEY or STABILITY_API_KEY == "sk-MYAPIKEY":
        print("     Warning: STABILITY_API_KEY not configured.")
        print("   Image generation will not work without a valid API key")
        print("   Get free credits at: https://platform.stability.ai/")
        print()
    
    # 1. Get post content
    print("📝 What do you want to post?")
    print("   (press Enter for default)")
    generated_text = input("Enter your post text: ").strip()
    
    if not generated_text:
        generated_text = "Check out our new Malware Analysis lab at Adaptlearn! 🛡️ #CyberSecurity"
        print(f"   Using default: {generated_text}")
    
    print()
    print("✅ Post content ready!")
    
    # 2. Ask if user wants to generate an image
    print("\n🔥 Ready to post to LinkedIn? (y/n): ", end="")
    if input().lower() != 'y':
        print("   Post cancelled.")
        exit(0)
    
    # 3. Image options
    print("\n📸 Image options:")
    print("   1. Generate image using AI (Stability AI)")
    print("   2. Use existing image file")
    print("   3. Post without image")
    print()
    
    choice = input("Choose (1/2/3): ").strip()
    image_path = None
    
    if choice == "1":
        if not STABILITY_API_KEY or STABILITY_API_KEY == "sk-MYAPIKEY":
            print("\n⚠️  API Key not configured. Skipping image generation.")
            print("   Set STABILITY_API_KEY in your .env file")
        else:
            # Generate image using AI
            image_prompt = input("\n📝 Describe the image you want: ").strip()
            if image_prompt:
                image_path = generate_ai_image(image_prompt)
            else:
                print("   No prompt provided. Using default...")
                image_path = generate_ai_image(DEFAULT_IMAGE_PROMPT)
    
    elif choice == "2":
        # Use existing image
        image_file = input("\n📁 Enter image file path: ").strip()
        if image_file and os.path.exists(image_file):
            # Validate it's an image
            valid_formats = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
            if image_file.lower().endswith(valid_formats):
                image_path = image_file
                print(f"   ✅ Image selected: {image_file}")
            else:
                print(f"   ❌ Unsupported format. Supported: {', '.join(valid_formats)}")
        else:
            print(f"   ❌ File not found: {image_file}")
    
    elif choice != "3":
        print("   ❌ Invalid choice. Using option 3 (no image).")
    
    # 4. Confirm and post
    print("\n" + "=" * 60)
    print("📋 Post Summary:")
    print(f"   Text: {generated_text[:50]}{'...' if len(generated_text) > 50 else ''}")
    print(f"   Image: {'Yes' if image_path else 'No'}")
    print("=" * 60)
    
    print("\n❓ Publish this post to LinkedIn? (y/n): ", end="")
    if input().lower() == 'y':
        success = post_to_linkedin(generated_text, image_path)
        if success:
            print("\n All done! Check your LinkedIn profile.")
        else:
            print("\n Post failed. Please check your settings and try again.")
    else:
        print("   Post cancelled by user.")
    
    print()