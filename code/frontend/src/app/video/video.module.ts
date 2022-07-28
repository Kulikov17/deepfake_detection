import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TuiButtonModule, TuiLoaderModule } from '@taiga-ui/core';
import { TuiInputFileModule } from '@taiga-ui/kit';

import { VideoComponent } from './components/video.component';
import { VideoClassPipe } from './pipes/video-class.pipe';

@NgModule({
  declarations: [
    VideoComponent,
    VideoClassPipe,
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    TuiButtonModule,
    TuiInputFileModule,
    TuiLoaderModule,
  ],
  exports: [
    VideoComponent,
  ],
})
export class VideoModule { }