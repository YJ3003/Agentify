"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { 
    onAuthStateChanged, 
    User, 
    signInWithPopup, 
    GithubAuthProvider, 
    signOut as firebaseSignOut,
    browserLocalPersistence,
    setPersistence,
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    linkWithPopup
} from "firebase/auth";
import { auth, githubProvider } from "@/lib/firebase";
import { useRouter } from "next/navigation";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signInWithGithub: () => Promise<void>;
  signInWithEmail: (email: string, pass: string) => Promise<void>;
  signUpWithEmail: (email: string, pass: string) => Promise<void>;
  linkWithGithub: () => Promise<void>;
  signOut: () => Promise<void>;
  getToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  signInWithGithub: async () => {},
  signInWithEmail: async () => {},
  signUpWithEmail: async () => {},
  linkWithGithub: async () => {},
  signOut: async () => {},
  getToken: async () => null,
});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Ensure persistence is set (firebase default is usually local, but explicit is good)
    setPersistence(auth, browserLocalPersistence).catch(console.error);

    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const signInWithGithub = async () => {
    try {
        console.log("Starting GitHub Sign In...");
        // Force account selection/re-authentication
        githubProvider.setCustomParameters({ prompt: 'select_account' });
        githubProvider.addScope('repo');
        const result = await signInWithPopup(auth, githubProvider);
        console.log("Firebase Popup Finished", result.user.uid);
        
        const credential = GithubAuthProvider.credentialFromResult(result);
        const token = credential?.accessToken;
        const user = result.user;
        const idToken = await user.getIdToken();
        
        console.log("GitHub Access Token present?", !!token);
        
        if (token) {
            console.log("Syncing GitHub token with backend...");
            // Import dynamically or assume it's available
            const api = await import("@/lib/api");
            await api.syncGithubToken(token, idToken);
            console.log("GitHub token synced successfully.");
        } else {
            console.error("No GitHub access token returned from credential.");
        }
    } catch (error) {
        console.error("Error signing in with GitHub", error);
        throw error;
    }
  };

  const signInWithEmail = async (email: string, pass: string) => {
      await signInWithEmailAndPassword(auth, email, pass);
  };

  const signUpWithEmail = async (email: string, pass: string) => {
      await createUserWithEmailAndPassword(auth, email, pass);
  };

  const linkWithGithub = async () => {
    if (!auth.currentUser) return;
    try {
        githubProvider.setCustomParameters({ prompt: 'select_account' });
        githubProvider.addScope('repo');
        const result = await linkWithPopup(auth.currentUser, githubProvider);
        const credential = GithubAuthProvider.credentialFromResult(result);
        const token = credential?.accessToken;
        const user = result.user;
        const idToken = await user.getIdToken();
        
        if (token) {
             const api = await import("@/lib/api");
             await api.syncGithubToken(token, idToken);
        }
        // Force refresh user state
        setUser({...user}); 
    } catch (error) {
        console.error("Error linking GitHub", error);
        throw error;
    }
  };

  const signOut = async () => {
    try {
        await firebaseSignOut(auth);
        router.push("/");
    } catch (error) {
        console.error("Error signing out", error);
    }
  };

  const getToken = async () => {
      if (!user) return null;
      return await user.getIdToken();
  }

  return (
    <AuthContext.Provider value={{ user, loading, signInWithGithub, signInWithEmail, signUpWithEmail, linkWithGithub, signOut, getToken }}>
      {children}
    </AuthContext.Provider>
  );
};
