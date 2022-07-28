import { ActionReducerMap, MetaReducer } from "@ngrx/store";
import { environment } from "src/environments/environment";
import { VideoEffects } from "./video/video.effects";
import { videoReducer } from "./video/video.reducer";

export interface IState {
}

export const reducers: ActionReducerMap<IState> = {
  video: videoReducer,
}

export const metaReducers: MetaReducer<IState>[] = !environment.production ? [] : []

export const effects = [
  VideoEffects,
]