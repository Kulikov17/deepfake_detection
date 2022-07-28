import { Action, createFeatureSelector, createReducer, createSelector, on } from '@ngrx/store';
import { VideoClass } from '../shared/models/video';
import { videoActions } from './video.actions';

export const VIDEO_STATE_KEY = 'video';

interface IVideoState {
  videoClass: VideoClass | null;
}

const initialState: IVideoState = {
  videoClass: null,
}

const reducer = createReducer(
  initialState,
  on(videoActions.predictVideoSuccess, (state, { videoClass }) => ({...state, videoClass})),
  on(videoActions.clearVideoStateSuccess, (state) => ({...state, videoClass: null})),
)

export function videoReducer(state: IVideoState, action: Action): IVideoState {
  return reducer(state, action);
}

const videoStateSelector = createFeatureSelector<IVideoState>(VIDEO_STATE_KEY);

export const videoSelectors = {
  videoClass: createSelector(videoStateSelector, (state: IVideoState): VideoClass | null => state.videoClass),
}