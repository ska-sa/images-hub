import { Component } from '@angular/core';
import { AuthService, UserInfo } from '../../services/auth.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UserService } from '../../services/user.service';
import { User } from '../../interfaces/user';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})

export class SignInComponent {
  signInForm: FormGroup = new FormGroup({});

  emailRegex: string = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$";

  userProfile: UserInfo | null = null;
  isSignedIn: boolean = false;

  constructor(private router: Router, private userService: UserService, private readonly authService: AuthService) {
    
    this.authService.userProfile$.subscribe((profile) => {
      this.userProfile = profile;
    });
    this.authService.isLoggedIn$.subscribe((isLoggedIn) => {
      this.isSignedIn = isLoggedIn;
    });
  
    
  }

  ngOnInit(): void {
    this.signInForm = new FormGroup({
      email: new FormControl("", [
        Validators.required, 
        Validators.pattern(this.emailRegex)
      ])
    });
  }

  get email() {
    return this.signInForm.get('email');
  }

  signIn(): void {
    this.userService.signIn(this.email?.value).subscribe({
      next: (user: User) => {
        //console.log(user);
        this.userService.setUser(user);
        let routerUrl: string = user.type == 0 ? "/guest/browse-images" : "/administrator/browse-requests";
        this.router.navigate([routerUrl]);
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  signInWithGoogle(): void {
    if (this.authService.email=='')
      this.authService.signIn();

    //console.log(this.emailWithGoogle);
    let emailAddress = '';
    emailAddress = this.emailWithGoogle;
    if (this.emailWithGoogle == null) {
      return
    }
    this.userService.signIn(emailAddress).subscribe({
      next: (user: User) => {
        //console.log(user);
        this.userService.setUser(user);
        let routerUrl: string = user.type == 0 ? "/guest/browse-images" : "/administrator/browse-requests";
        this.router.navigate([routerUrl]);
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  signOutWithGoogle() {
    this.authService.signOut();
  }

  get emailWithGoogle() {
    return this.authService.email;
  }
}
