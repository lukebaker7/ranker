from datetime import datetime, timezone
import uuid
from flask import render_template, flash, redirect, url_for, request, g, \
    current_app
from flask_login import current_user, login_required
import sqlalchemy as sa
from app import db
from app.main.forms import EditProfileForm, ItemForm, ItemUpdateForm, RatingForm
from app.models import User, Item, reviews, Rating
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    # item = db.session.execute(sa.select(Item).order_by(sa.func.random()).limit(1)).scalar_one_or_none()
    # if item is None:
    #     flash('No items found!')
    #     return render_template('index.html')
        
    # form = RatingForm()
    # if form.validate_on_submit():
    #     rating = Rating(rating=form.rating.data, item_id=form.item_id.data, id=str(uuid.uuid4()))
    #     rated_item = db.session.get(Item, form.item_id.data)
    #     if rated_item:
    #         rated_item.reviews += 1
    #         db.session.add(rating)
    #         db.session.commit()
    #         flash('Rating submitted')
    #     return redirect(url_for('main.index'))
    # form.item_id.data = item.id
    # score = item.get_score()
    return render_template('index.html')

@bp.route('/update_items', methods=['GET', 'POST'])
def update_item():
    item = db.first_or_404(sa.select(Item).where(Item.name == None).limit(1))#Get incomplete items
    if item is None:
        return render_template('errors.404.html')
    form = ItemUpdateForm()
    if form.validate_on_submit():
        updated_item = Item.query.get(form.item_id.data)
        updated_item.name = form.name.data
        updated_item.description = form.description.data
        db.session.commit()
        return redirect(url_for('main.update_item'))

    form.item_id.data = item.id
    form.url.data = item.photo_url

    return render_template('update_items.html', item=item, form=form)

@bp.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'GET':
        form = ItemForm()
        return render_template('add_item.html', form=form)
    data = request.form
    if 'url' in data:
        item_id = str(uuid.uuid4())
        item = Item(photo_url=data['url'], id=item_id)
        db.session.add(item)
        db.session.commit()
        return {
            "statusCode": 200,
            "body": f"{item_id}: Your item is now live"
        } if request.is_json else redirect(url_for('main.add_item'))
    return {
        "statusCode": 400,
        "body": "Please provide all required fields"
    }

@bp.route('/add_review/<item_id>', methods=['POST', 'PUT'])
def add_review(item_id):
    data = request.form
    rating = int(data['rating'])
    item = Item.query.get(item_id)
    if item is None:
        return {
            "statusCode": 404,
            "body": "Item not found"
        }
    item.reviews += 1
    rating_id = str(uuid.uuid4())
    rate = Rating(rating=rating, item_id=item_id, id=rating_id)
    db.session.add(rate)
    db.session.commit()
    return {
        "statusCode": 200,
        "body": f"Review added to {item_id}",
        "rating_id": rating_id
    }
@bp.route('/items/review/<item_id>', methods=['GET'])
def reviews(item_id):
    item = Item.query.get(item_id)
    if item is None:
        return {
            "statusCode": 404,
            "body": "Item not found"
        }
    result = []
    reviews = db.session.execute(sa.select(Rating).where(Rating.item_id == item_id)).scalars()
    
    for rating in reviews:
        result.append(rating.rating)
    
    return {
        "statusCode": 200,
        "ratings": result
        # "body": [review.rating for review in reviews]
    }

@bp.route('/items/v2', methods=['GET'])
def get_items():
    item = db.session.execute(
        sa.select(Item).order_by(sa.func.random()).limit(1)
    ).scalar_one_or_none()
    
    if item is None:
        return {'error': 'No items found'}, 404
        
    return {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'photo_url': item.photo_url,
        'score': item.get_score()
    }

@bp.route('/items', methods=['GET']) #Needs to just return the items
def items():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', current_app.config['POSTS_PER_PAGE'], type=int)
    
    # Simple query for items
    query = sa.select(Item)
    
    # Execute with pagination
    items_page = db.paginate(
        query,
        page=page,
        per_page=limit,
        error_out=False
    )
    
    return {
        "statusCode": 200,
        "data": [item.to_dict() for item in items_page.items],
        "previous_url": url_for('main.items', page=items_page.prev_num) 
            if items_page.has_prev else None,
        "next_url": url_for('main.items', page=items_page.next_num)
            if items_page.has_next else None
    }