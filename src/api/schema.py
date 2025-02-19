import operator
import typing

import strawberry
from strawberry.schema.config import StrawberryConfig

from src.api.models.recipe import Section, Recipe
from src.recommendations.model_initializer import calculate_recommendation_models
from src.recommendations.recommendation_updater import update_recommendations
from src.recommendations.recommender import get_recipes_sections, \
    get_similar_recipes


def default_resolver(root, field):
    try:
        return operator.getitem(root, field)
    except KeyError:
        return getattr(root, field)


config = StrawberryConfig(
    default_resolver=default_resolver,
    auto_camel_case=False
)


def sections_resolver(user_id: str) -> typing.List[Section]:
    return get_recipes_sections(user_id)


def similar_recipes_resolver(recipe_index: int, user_id: str) -> typing.List[Section]:
    return get_similar_recipes(recipe_index, user_id)


def update_recommendations_feed(user_id: str) -> str:
    return update_recommendations(user_id)


def calculate_models() -> None:
    calculate_recommendation_models()
    return


@strawberry.type
class Query:
    sections: typing.List[Section] = strawberry.field(resolver=sections_resolver)
    similar_recipes: typing.List[Section] = strawberry.field(resolver=similar_recipes_resolver)


@strawberry.type
class Mutation:
    update_user_recommendations = strawberry.mutation(resolver=update_recommendations_feed)
    calculate_models = strawberry.mutation(resolver=calculate_models)


schema = strawberry.Schema(query=Query, mutation=Mutation, config=config)
