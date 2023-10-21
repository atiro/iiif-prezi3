from ..loader import monkeypatch_schema
from ..skeleton import (AccompanyingCanvas, Annotation, AnnotationPage, Canvas,
                        PlaceholderCanvas, ResourceItem, ServiceItem, ServiceItem1)


class AddImage:

    def add_image(self, image_url, anno_id=None, anno_page_id=None, **kwargs):
        """Adds an image to an existing canvas.

        Args:
            image_url (str): An HTTP URL which points to the image.
            anno_id (str): An HTTP URL for the annotation to which the image will be attached.
            anno_page_id (str): An HTTP URL for the annotation page to which the annotation will be attached.

        Returns:
            anno_page (AnnotationPage): the AnnotationPage with an Annotation and ResourceItem attached.
        """
        body = ResourceItem(id=image_url, type='Image', **kwargs)
        annotation = Annotation(id=anno_id, body=body, target=self.id, motivation='painting', type='Annotation')
        anno_page = AnnotationPage(id=anno_page_id, type='AnnotationPage', items=[annotation])
        if not self.items:
            self.items = list()
        self.items.append(anno_page)
        return anno_page

    def add_choice_image(self, image_url, **kwargs):
        alt_image = ResourceItem(id=image_url, type='Image', **kwargs)
        self.items[0].items[0].body.items.append(alt_image)

    def add_choice_iiif_image(self, image_url, **kwargs):

        alt_image = ResourceItem(id="http://example.com", type="Image")

        infoJson = alt_image.set_hwd_from_iiif(image_url)

        # Will need to handle IIIF 2...
        if 'type' not in infoJson:
            # Assume v2

            # V2 profile contains profile URI plus extra features
            profile = ''
            for item in infoJson['profile']:
                if isinstance(item, str):
                    profile = item
                    break

            service = ServiceItem1(id=infoJson['@id'], profile=profile, type="ImageService2")
            alt_image.service = [service]
            alt_image.id = f'{infoJson["@id"]}/full/full/0/default.jpg'
            alt_image.format = "image/jpeg"
        else:
            service = ServiceItem(id=infoJson['id'], profile=infoJson['profile'], type=infoJson['type'])
            alt_image.service = [service]
            alt_image.id = f'{infoJson["id"]}/full/max/0/default.jpg'
            alt_image.format = "image/jpeg"

        # hardcoded - AnnotationPage 0 / annotation 0 / body / items
        self.items[0].items[0].body.items.append(alt_image)

monkeypatch_schema([Canvas, AccompanyingCanvas, PlaceholderCanvas], AddImage)
