import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, Header, Depends
from typing import Optional
import os

# Initialize Firebase Admin
try:
    # Use default credentials or service account path from env
    # USER UPDATE: Use explicit path backend/firebase_service_account.json if env not set
    cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    if not cred_path:
        possible_path = os.path.join("backend", "firebase_service_account.json")
        if os.path.exists(possible_path):
            cred_path = possible_path
    
    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        # Fallback to default google credentials
        # NOTE: This often fails locally without explicit project ID or ADC
        print("Warning: No service account found. Using default creds (may fail if project_id missing).")
        firebase_admin.initialize_app()
    print("Firebase Admin Initialized")
except ValueError:
    print("Firebase app already initialized")

def verify_token(authorization: Optional[str] = Header(None)) -> str:
    print(f"DEBUG: verify_token called with header length: {len(authorization) if authorization else 0}")
    if not authorization:
        print("DEBUG: No authorization header")
        raise HTTPException(status_code=401, detail="No authorization header")
    
    if not authorization.startswith("Bearer "):
         print("DEBUG: Invalid header format")
         raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    token = authorization.split("Bearer ")[1]
    
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        # print(f"DEBUG: Token Verified for UID: {uid}")
        return uid
    except auth.ExpiredIdTokenError:
        print("DEBUG: Token Expired")
        raise HTTPException(status_code=401, detail="Token expired")
    except auth.InvalidIdTokenError as e:
         print(f"DEBUG: Invalid Token: {e}")
         raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Could not verify token")
