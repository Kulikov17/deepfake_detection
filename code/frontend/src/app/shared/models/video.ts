export type VideoClass = 'real' | 'fake' | 'no-face';

export interface VideoPredictResponse {
  videoClass: VideoClass;
}