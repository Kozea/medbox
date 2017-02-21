from urllib.parse import quote

from top_model import db
from top_model.ext.flask import FlaskTopModel
from top_model.filesystem import ProductPhotoCIP
from top_model.webstore import Product, Labo
from unrest import UnRest


class Hydra(FlaskTopModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config['CLIENT_ID'] = 4
        self.config['BASE_IMAGE_URL'] = (
            'https://static.pharminfo.fr/images/cip/{cip}/{name}.{ext}')
        self.config['SQLALCHEMY_DATABASE_URI'] = (
            'pgfdw://hydra@localhost/hydra')
        self.config.from_envvar('MEDBOX_SETTINGS', silent=True)
        self.configure_db(self.config['SQLALCHEMY_DATABASE_URI'])


def filter_query(query):
    return query.filter_by(client_id=app.config['CLIENT_ID'])


app = Hydra(__name__)


rest = UnRest(app, db.session)
rest(Labo, only=('label',))
product_api = rest(Product, query=filter_query, only=(
    'product_id', 'title', 'description', 'cip', 'resip_labo_code',
    'type_product'))
image_api = rest(ProductPhotoCIP, only=('cip', 'name', 'ext'))


@image_api.declare('GET')
def get_image(payload, cip, name, ext):
    result = image_api.get(payload, cip=cip)
    for obj in result['objects']:
        obj['name'] = quote(obj['name'])
        obj['url'] = app.config['BASE_IMAGE_URL'].format(**obj)
    return result


@product_api.declare('GET')
def get_product(payload, product_id):
    products = (
        Product.query
        .filter_by(cip=str(product_id))
        .filter_by(client_id=app.config['CLIENT_ID'])
        .all())
    if products:
        return product_api.get(payload, product_id=products[0].product_id)
    else:
        return {'objects': [], 'occurences': 0}
