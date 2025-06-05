import base64


def encode_safe_string(input_str):
    encoded = base64.urlsafe_b64encode(input_str.encode()).decode()
    return encoded.rstrip("=")  # Optional: remove padding to avoid "="


def decode_safe_string(encoded_str):
    # Add padding back before decoding
    padding = "=" * ((4 - len(encoded_str) % 4) % 4)
    return base64.urlsafe_b64decode(encoded_str + padding).decode()


init_script = """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                window.navigator.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                """
