---
description: Version a planning doc - creates _v{n+1} and archives current to deprecated/
arguments: <file_path>
---

# Document Versioning

I'll help you version the planning document: **{{ARG1}}**

## Step 1: Analyze Current File

<function_calls>
<invoke name="Bash">
<parameter name="command">
FILE_PATH="{{ARG1}}"

if [ ! -f "$FILE_PATH" ]; then
  echo "❌ ERROR: File not found: $FILE_PATH"
  exit 1
fi

DIR=$(dirname "$FILE_PATH")
BASENAME=$(basename "$FILE_PATH")
FILENAME="${BASENAME%.*}"
EXTENSION="${BASENAME##*.}"

if [[ $FILENAME =~ _v([0-9]+)$ ]]; then
  CURRENT_VERSION="${BASH_REMATCH[1]}"
  BASE_NAME="${FILENAME%_v*}"
else
  CURRENT_VERSION="0"
  BASE_NAME="$FILENAME"
fi

NEW_VERSION=$((CURRENT_VERSION + 1))
NEW_FILENAME="${BASE_NAME}_v${NEW_VERSION}.${EXTENSION}"
NEW_PATH="${DIR}/${NEW_FILENAME}"

echo "📄 Current file: $FILE_PATH"
echo "📌 Current version: v$CURRENT_VERSION"
echo "✨ New version will be: v$NEW_VERSION"
</parameter>
</invoke>