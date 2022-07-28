import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'videoClass'
})
export class VideoClassPipe implements PipeTransform {

  transform(type: string | null): string {
    let videoClassInfo = 'Видео не является поддельным';
    
    switch(type) {
      case 'real': 
        videoClassInfo = 'Видео не является поддельным';
        break;
      case 'fake': 
        videoClassInfo = 'Видео является поддельным';
        break;
      case 'no_face': 
        videoClassInfo = 'На видео не обнаружены лица';
        break;
      case 'medium-fake': 
        videoClassInfo = 'Сложно определить класс видео'
        break;
      default:
        videoClassInfo = 'Возникла ошибка определения класса видео. Попробуйте еще раз'
    }

    return videoClassInfo
  }

}
