import { createAction } from "@ngrx/store";
import { VideoClass } from '../shared/models/video';

export const videoActions = {
  predictVideo: createAction('[VIDEO] Predict video', (file: File) => ({file})),
  predictVideoSuccess: createAction('[VIDEO] Predict video success', (videoClass: VideoClass) => ({videoClass})),
  clearVideoState: createAction('[VIDEO] Clear video state'),
  clearVideoStateSuccess: createAction('[VIDEO] Clear video state success'),
}