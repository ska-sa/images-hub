import { Injectable } from '@angular/core';
import { AuthConfig, OAuthService } from 'angular-oauth2-oidc';
import { BehaviorSubject } from 'rxjs';
import { environment } from 'src/environments/environment.development';

const authCodeFlowConfig: AuthConfig = {
  // Url of the Identity Provider
  issuer: 'https://accounts.google.com',
  // strict discovery document disallows urls which not start with issuers url
  strictDiscoveryDocumentValidation: false,
  // URL of the SPA to redirect the user to after login
  redirectUri: window.location.origin + '/sign-in',
  // The SPA's id. The SPA is registerd with this id at the auth-server
  clientId: environment.clientId,
  // set the scope for the permissions the client should request
  scope: 'openid profile email',
  showDebugInformation: true,
  oidc: false
};

export interface UserInfo {
  info: {
    email: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private userProfileSubject = new BehaviorSubject<UserInfo | null>(null);
  private isLoggedInSubject = new BehaviorSubject<boolean>(false);

  constructor(private readonly oAuthService: OAuthService) {
    oAuthService.configure(authCodeFlowConfig);
    oAuthService.loadDiscoveryDocument().then(() => {
      oAuthService.tryLoginImplicitFlow().then(() => {
        if (!oAuthService.hasValidAccessToken()) {
          oAuthService.initLoginFlow();
        } else {
          this.loadUserProfile();
        }
      });
    });
  }

  loadUserProfile() {
    this.oAuthService.loadUserProfile().then((userProfile) => {
      this.userProfileSubject.next(userProfile as UserInfo);
      this.isLoggedInSubject.next(true);
    }).catch(error => {
      console.error('Error loading user profile', error);
      this.isLoggedInSubject.next(false);
    });
  }

  signIn() {
    this.oAuthService.initLoginFlow();
  }

  signOut() {
    this.oAuthService.logOut();
    this.userProfileSubject.next(null);
    this.isLoggedInSubject.next(false);
  }

  get userProfile$() {
    return this.userProfileSubject.asObservable();
  }

  get isLoggedIn$() {
    return this.isLoggedInSubject.asObservable();
  }

  get email() {
    let claims = this.oAuthService.getIdentityClaims();
    return claims ? claims['email'] : null;
  }
}