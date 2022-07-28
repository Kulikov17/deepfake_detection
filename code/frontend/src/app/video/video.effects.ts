import { Inject, Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Actions, ofType, createEffect } from "@ngrx/effects";
import { catchError, map, mergeMap, tap } from "rxjs/operators";
import { EMPTY } from "rxjs";
import { TuiNotification, TuiAlertService } from '@taiga-ui/core';
import { videoActions } from "./video.actions";
import { VideoPredictResponse, VideoClass } from "../shared/models/video";

export const ERROR_LABEL_PREDICT_VIDEO = 'Не удалось проверить класс видео';
export const ERROR_MESSAGE_PREDICT_VIDEO = 'Во время проверки видео произошла ошибка, повторите попытку позже';

@Injectable()
export class VideoEffects {

  constructor(
    private readonly actions$: Actions,
    private readonly http: HttpClient,
    @Inject(TuiAlertService)
    private readonly alertService: TuiAlertService,
  ) {}

  predictVideo$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(videoActions.predictVideo),
      map(({file}) => {
        const formData = new FormData();
        formData.append("file", file);
        return formData
      }),
      mergeMap((formData: FormData) => this.http
        .post<VideoPredictResponse>('/api/video/predict', formData)
        .pipe(
          map(({videoClass}) => videoActions.predictVideoSuccess(videoClass)),
          catchError((error) => {
            this.alertService.open(`${ERROR_MESSAGE_PREDICT_VIDEO}: ${error}`, {
              label: ERROR_LABEL_PREDICT_VIDEO,
              status: TuiNotification.Error,
            }).subscribe();
            
            return EMPTY;
          }),
        )
      ),
    )
  });
}