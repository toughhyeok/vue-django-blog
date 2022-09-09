def obj_to_post(obj, flag=True):
    """
    obj의 각 속성을 serialize 해서, dict로 변환한다.
    serialize: python object --> (기본 타입) int, float, str
    :param obj:
    :param flag: True (모두 보냄, /api/post/99/ 용),
                 False (일부 보냄, /api/post/list/ 용)
    :return:
    """
    post = dict(vars(obj))
    if obj.category:
        post['category'] = obj.category.name
    else:
        post['category'] = 'NoCategory'

    if obj.tags:
        post['tags'] = [tag.name for tag in obj.tags.all()]
    else:
        post['tags'] = []

    if obj.image:
        post['image'] = obj.image.url
    else:
        post['image'] = 'https://via.placeholder.com/900x300/'

    if obj.update_dt:
        post['update_dt'] = obj.update_dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        post['update_dt'] = '9999-12-31 00:00:00'

    del post['_state'], post['category_id'], post['create_dt'], post['_prefetched_objects_cache'] # noqa
    if not flag:
        del post['tags'], post['update_dt'], post['description'], post['content']   # noqa

    return post


def prev_next_post(obj):
    try:
        prev_obj = obj.get_previous_by_update_dt()
        prev_dict = {
            'id': prev_obj.id,
            'title': prev_obj.title,
        }
    except obj.DoesNotExist:
        prev_dict = {}

    try:
        next_obj = obj.get_next_by_update_dt()
        next_dict = {
            'id': next_obj.id,
            'title': next_obj.title,
        }
    except obj.DoesNotExist:
        next_dict = {}

    return prev_dict, next_dict
