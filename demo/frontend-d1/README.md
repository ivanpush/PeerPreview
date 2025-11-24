# PeerPreview Demo (D1)

Static React prototype for user touchpoint testing.

## Purpose

This is a **non-functional demo** to validate UX flows before building the real application. Uses mock data loaded from static JSON files.

## Structure

```
frontend-d1/
├── src/
│   ├── pages/           # 3 main screens
│   ├── components/      # Reusable UI components
│   └── utils/           # Mock data loader
├── public/static/       # Mock JSON data
└── package.json
```

## Setup

```bash
cd demo/frontend-d1
npm install
npm run dev
```

Open http://localhost:5173

## Mock Data

- `manuscript_demo.json` - Parsed paper sections
- `issues_demo.json` - AI-detected issues with rewrite suggestions

## Screens

1. **UploadScreen** - Upload PDF (fake, just transitions)
2. **ProcessScreen** - Show "analyzing..." animation
3. **ReviewScreen** - Main UI with manuscript view + issues panel

## Next Steps

After user feedback:
1. Build real frontend in `/frontend`
2. Connect to real backend APIs
3. Implement actual LLM agent workflows
