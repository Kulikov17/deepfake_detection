import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Store } from '@ngrx/store';
import { delay, tap } from 'rxjs/operators';
import { videoActions } from '../video.actions';
import { videoSelectors } from '../video.reducer';


@Component({
  selector: 'app-video',
  templateUrl: './video.component.html',
  styleUrls: ['./video.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class VideoComponent implements OnInit {
    isVideoLoad = false;
    isVideoPredictBtn = false;
    isVideoClass = this.store$.select(videoSelectors.videoClass);

    readonly videoControl = new FormControl();

    constructor (
        private readonly store$: Store
    ) {}

    ngOnInit(): void {
        this.videoControl.valueChanges.pipe(
            tap(file => {
                this.isVideoLoad = file? true : false;
                this.isVideoPredictBtn = this.isVideoLoad;
            }),
            delay(100),
            tap(file => file ? this.setVideo() : this.store$.dispatch(videoActions.clearVideoStateSuccess())),
        ).subscribe();
    }

    private setVideo() {
        const videoNode = document.querySelector('video');
        if (videoNode) {
            const fileURL = URL.createObjectURL(this.videoControl.value);
            videoNode.src = fileURL;
        }
    }

    onPredictVideoClass() {
        if (this.videoControl.value) {
            this.isVideoPredictBtn = false;
            this.store$.dispatch(videoActions.predictVideo(this.videoControl.value));
        }
    }
}
