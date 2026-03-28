# LinkedIn AI Content Poster

An automated tool to generate AI-powered images and post them to LinkedIn.

## Features

- 🤖 Generate ultra-realistic images using Stability AI Ultra model
- 🔗 Automatic LinkedIn posting with image attachment
- 📝 Custom post content
- 🔐 Secure API key management

## Prerequisites

- Python 3.8+
- LinkedIn Developer Account with valid OAuth token
- Stability AI API key (free credits available)

## Setup

### 1. Clone/Download the Repository

```bash
git clone <repository-url>
cd adaptlearn_aggregator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your actual API keys:

```bash
cp .env.example .env
```

Edit `.env` and add:
- `LINKEDIN_TOKEN` - Get from [LinkedIn Developers](https://www.linkedin.com/developers/)
- `STABILITY_API_KEY` - Get from [Stability AI](https://platform.stability.ai/)

### 4. Security

⚠️ **IMPORTANT**: Never commit `.env` to version control!

- `.env` file is protected with file-level permissions (owner access only)
- `.env` is excluded from git tracking via `.gitignore`
- `.env.example` provides a template for configuration

## Usage

```bash
python main.py
```

Follow the prompts to:
1. Enter your post content
2. Choose image generation or upload
3. Confirm and publish to LinkedIn

## Project Structure

```
adaptlearn_aggregator/
├── main.py                 # Main application
├── requirements.txt        # Python dependencies
├── .env                    # (SENSITIVE) API keys - never commit
├── .env.example           # Configuration template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Security Best Practices

✅ **What we do:**
- Store sensitive data in `.env` (not in code)
- Restrict `.env` file permissions to owner only
- Exclude `.env` from git version control
- Provide `.env.example` as safe template

✅ **What you should do:**
- Never share your `.env` file
- Rotate API keys periodically
- Keep git repository private or at least don't commit credentials
- Review permissions on `.env` file

## Error Handling

The application includes comprehensive error handling for:
- Missing or invalid API tokens
- Network timeouts
- File size validation
- LinkedIn API errors
- Image generation failures

## Supported Image Formats

- JPEG/JPG
- PNG
- GIF
- WebP (recommended - smaller file size)

Maximum file size: 10MB

## API Documentation

- [LinkedIn API v2](https://docs.microsoft.com/en-us/linkedin/shared/api-reference/api-reference)
- [Stability AI Documentation](https://platform.stability.ai/docs/getting-started)

## License

[Your License Here]

## Support

For issues or questions, please open an issue in the repository.
