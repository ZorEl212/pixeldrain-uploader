# Pixeldrain File Uploader

A Python script to upload local files to **Pixeldrain** from CLI.

---

## Features

- **Authentication**: Uses Pixeldrain API Key for secure uploads.
- **SNI Support**: Custom SNI (Server Name Indication) hostname configuration to bypass SSL/TLS issues.
- **Upload Progress**: Displays real-time upload progress.

---

## Requirements

Make sure you have the following dependencies installed:

- Python 3.6+
- Required Python libraries:
  - `requests`
  - `tqdm`
  - `urllib3`

Install the dependencies using:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Clone or download the script.
2. Run the script from the command line with the required arguments.

### Syntax
```bash
python upload_script.py <file_name> <api_key> [--sni-hostname <hostname>]
```

### Arguments:
- `file_name`: The name of the local file you want to upload.
- `api_key`: Your Pixeldrain API key (obtainable from your Pixeldrain account). API key can be set as an environment variable `PDUP_API_KEY`.
- `--sni-hostname` (optional): The hostname to use for the SNI field. Default is `pixeldrain.net`.


---

### Example

Upload a file named `example.txt` using your Pixeldrain API key:

```bash
python upload_script.py example.txt YOUR_API_KEY
```

If you encounter SSL/TLS issues, specify an SNI hostname:

```bash
python upload_script.py example.txt YOUR_API_KEY --sni-hostname t.me
```

---

## Sample Output

```plaintext
Uploading: 100%|███████████████████████████████████| 2.0M/2.0M [00:03<00:00, 630kB/s]
File uploaded successfully: https://pixeldrain.com/u/abc123def
```

---

## Troubleshooting

- **SSL/TLS Issues**: 
  - Try using a different SNI hostname (e.g., `pixeldra.in`) with the `--sni-hostname` option.

- **Invalid API Key**:
  - Double-check your Pixeldrain API key and ensure it’s valid.

- **File Not Found**:
  - Ensure the file exists in the specified path.

---

## License

This script is open-source and available under the MIT License. Contributions and feedback are welcome! 😊

---

## Author

Developed by [Yeasira Desalegn](https://github.com/ZorEl212).