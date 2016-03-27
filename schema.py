#!/usr/bin/env python3
# encoding: utf-8
import graphene


class Person(graphene.ObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    full_name = graphene.String()

    def resolve_full_name(self, args, info):
        return '{0.first_name} {0.last_name}'.format(self)


class CreatePerson(graphene.Mutation):
    ok = graphene.Boolean()
    person = graphene.Field(Person)

    @classmethod
    def mutate(cls, instance, args, info):
        person = Person(
            id='1002',
            first_name=args.get('firstName'),
            last_name=args.get('lastName')
        )
        ok = True
        return cls(ok=ok, person=person)

    class Input:
        first_name = graphene.String()
        last_name = graphene.String()


class Query(graphene.ObjectType):
    person = graphene.Field(Person, id=graphene.String())

    @graphene.resolve_only_args
    def resolve_person(self, id):
        return Person(id='1000', first_name='João', last_name='Dubas')


class Mutation(graphene.ObjectType):
    create_person = graphene.Field(CreatePerson)


Schema = graphene.Schema(query=Query, mutation=Mutation)

if __name__ == '__main__':
    import json
    query_rs = Schema.execute('''query {
        person(id:"1000") {
            firstName
            lastName
            fullName
        }
    }''')
    mutation_rs = Schema.execute('''mutation Mutation {
        createPerson(firstName:"Claudio", lastName:"Dubas") {
            person {
                id
                lastName
            }
            ok
        }
    }''')
    print(json.dumps(query_rs.data))
    print(json.dumps(mutation_rs.data))
