# Разведочный анализ: генерация логотипов базовой моделью Stable Diffusion
## Модель
Для ознакомления с возможностями генерации изображений использовали предобученную модель Stable Diffusion, ноутбук с кодом - [`notebooks/stable_diffusion_base_gen.ipynb`](notebooks/stable_diffusion_base_gen.ipynb).

## Примеры генераций
Использованные промпты и полученные генерации приведены в файле [`DATA.md`](DATA.md).

## Анализ
Модель имеет общее представление о том, как выглядят логотипы, способна стилизовать изображения с учетом сферы деятельности условной компании, других указанных в промпте требований. При этом на сгенерированных изображениях часто присутствуют текстоподобные элементы, однако сам текст зачастую деформирован, имеет ошибки или не несет смысловой нагрузки. Сами изображения также содержат различные артефакты, затрудняющие использование полученных изображений напрямую в качестве логотипов, однако могут быть использованы в качестве эскизов для дальнейшей ручной обработки.

*Примеры генераций (наведите курсор на изображение, чтобы увидеть prompt)*

![logos_1411/19.png](http://51.250.100.5/static/logos_1411/19.png "Coffee logo, featuring a mushroom cloud coming out of a cup, the cloud looks like brains, by mcbess, full colour print, vintage colours, 1960s")

![logos_1411/14.png](http://51.250.100.5/static/logos_1411/14.png "A fashion logo for a classic, timeless brand, featuring an elegant serif font with a sophisticated monogram and a minimalist graphic")

![logos_1411/5.png](http://51.250.100.5/static/logos_1411/5.png "Develop a logo for a music streaming platform curating dynamic and experimental music. Use vector illustrations, geometric shapes, and symmetrical elements for an intriguing logo. Subtly incorporate a headphone to symbolize the platform’s focus.")

Для улучшения качества может потребоваться отдельно подобрать промпты и параметры для генерации дизайнов логотипов и типографики; интеграцию текста в логотипы сделать в базовом виде или оставить для пользовательской доработки. В частности, необходимо будет подобрать базовые шаблоны промптов, которые можно будет использовать вместе с пользовательским вводом для получения качественных и релевантных генераций. Также для улучшения качества типографики и добавления возможности использовать при генерации пользовательские референсы можно попробовать разные методы дообучения моделей: Dreambooth, LoRA.