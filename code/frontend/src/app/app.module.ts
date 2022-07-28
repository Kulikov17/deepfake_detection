import { NgDompurifySanitizer } from "@tinkoff/ng-dompurify";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { TuiRootModule, TuiDialogModule, TUI_SANITIZER, TuiButtonModule, TuiAlertModule} from "@taiga-ui/core";
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { TuiInputFileModule, TuiInputFilesModule } from '@taiga-ui/kit';
import { FormsModule }   from '@angular/forms'; 
import { ReactiveFormsModule }   from '@angular/forms';

import { AppComponent } from './app.component';
import { ApiHttpInterceptor } from './core/api.interceptor';
import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';
import { effects, metaReducers, reducers } from "./meta-reducer";
import { VideoModule } from "./video/video.module";
import { AppHeaderComponent } from './app-header/app-header.component';

@NgModule({
  declarations: [
    AppComponent,
    AppHeaderComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    TuiRootModule,
    BrowserAnimationsModule,
    TuiDialogModule,
    TuiAlertModule,
    TuiButtonModule,
    TuiInputFileModule,
    TuiInputFilesModule,
    FormsModule,
    ReactiveFormsModule,
    StoreModule.forRoot(reducers, {
      metaReducers
    }),
    EffectsModule.forRoot(effects),
    VideoModule,
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: ApiHttpInterceptor, multi: true },
    { provide: TUI_SANITIZER, useClass: NgDompurifySanitizer }
  ],
  bootstrap: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule { }
