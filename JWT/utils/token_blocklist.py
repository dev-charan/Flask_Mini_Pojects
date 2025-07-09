token_blocklist = set()

def add_token_to_blocklist(jti):
    token_blocklist.add(jti)

def is_token_revoked(jwt_payload):
    return jwt_payload["jti"] in token_blocklist
