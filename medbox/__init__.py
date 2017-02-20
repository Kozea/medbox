from top_model import db
from top_model.ext.flask import FlaskTopModel
from top_model.filesystem import ProductImage
from top_model.webstore import Product, Labo
from unrest import UnRest


class Hydra(FlaskTopModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config['CLIENT_ID'] = 4
        self.config['BASE_IMAGE_URL'] = (
            'https://static.pharminfo.fr/static/clients/{client_id}/'
            'images/product/{product_id}/{name}.{ext}')
        self.config['SQLALCHEMY_DATABASE_URI'] = (
            'pgfdw://hydra@localhost/hydra')
        self.config.from_envvar('MEDBOX_SETTINGS', silent=True)
        self.configure_db(self.config['SQLALCHEMY_DATABASE_URI'])


def filter_query(query):
    return query.filter_by(client_id=app.config['CLIENT_ID'])


app = Hydra(__name__)


rest = UnRest(app, db.session)
rest(
    Product, query=filter_query, only=(
        'product_id', 'title', 'description', 'cip', 'resip_labo_code',
        'type_product'))
rest(Labo, only=('label',))
image_api = rest(
    ProductImage, query=filter_query, only=('product_id', 'name', 'ext'))


@image_api.declare('GET')
def get(payload, client_id, product_id, name, ext):
    result = image_api.get(payload, product_id=product_id)
    for obj in result['objects']:
        obj['url'] = app.config['BASE_IMAGE_URL'].format(**obj)
    return result
