from voting_for_films import ns_films, col_films


class FilmDAO(object):
    def __init__(self):
        self.films = col_films

    def get_all(self, genre=None, actor=None):
        if genre and actor:
            return list(col_films.find({"genres": genre, "actors": actor}))
        if genre:
            return list(col_films.find({"genres": genre}))
        if actor:
            return list(col_films.find({"actors": actor}))
        return list(col_films.find())

    def get_one(self, id):
        film = col_films.find_one({"id": id})
        if film:
            return film
        ns_films.abort(404, "Film {} doesn't exist".format(id))

    def get_genres(self):
        return {"genres": col_films.distinct("genres")}

    def create(self, data):
        last_film = col_films.find().sort([('_id', -1)]).limit(1)[0]
        data["id"] = last_film["id"] + 1
        film = col_films.insert_one(data)
        _id = film.inserted_id
        return col_films.find_one({"_id": _id})

    def create_with_id(self, id, data):
        data["id"] = id
        if not col_films.find_one({"id": id}):
            film = col_films.insert_one(data)
            _id = film.inserted_id
            return col_films.find_one({"_id": _id})
        ns_films.abort(400, "Film {} already exist".format(id))

    def update(self, id, data):
        film = col_films.find_one_and_update({"id": id}, {"$set": data})
        if film:
            return col_films.find_one({"id": id})
        ns_films.abort(400, "Film {} doesn't exist".format(id))

    def delete(self, id):
        col_films.delete_one({"id": id})
