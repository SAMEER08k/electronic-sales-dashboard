import streamlit_authenticator as stauth

# List of plain text passwords
passwords = ["sameer123", "admin123"]

# Create Hasher object and hash the passwords
hasher = stauth.Hasher()
hashed_passwords = [hasher.hash(pw) for pw in passwords]

# Print the results
for i, hp in enumerate(hashed_passwords):
    print(f"Password {i+1} hash: {hp}")


