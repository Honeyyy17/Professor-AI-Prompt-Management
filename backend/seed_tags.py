
from app import create_app
from models import db, User, Prompt, PromptTag

def seed_tags():
    app = create_app()
    with app.app_context():
        # Get demo user
        user = User.query.filter_by(username='demo').first()
        if not user:
            print("Demo user not found. Please run seed first.")
            return

        # Create sample tags if they don't exist
        tag_data = [
            {'name': 'Production', 'color': '#10b981'},
            {'name': 'Research', 'color': '#3b82f6'},
            {'name': 'Draft', 'color': '#f59e0b'}
        ]
        
        tags = []
        for data in tag_data:
            tag = PromptTag.query.filter_by(name=data['name']).first()
            if not tag:
                tag = PromptTag(name=data['name'], color=data['color'])
                db.session.add(tag)
            tags.append(tag)
        
        db.session.flush()

        # Associate tags with prompts
        prompts = Prompt.query.filter_by(user_id=user.id).all()
        for i, prompt in enumerate(prompts):
            # Give each prompt a tag
            tag_to_add = tags[i % len(tags)]
            if tag_to_add not in prompt.tags:
                prompt.tags.append(tag_to_add)
                print(f"Added tag '{tag_to_add.name}' to prompt '{prompt.title}'")

        db.session.commit()
        print("Successfully seeded tags and associated them with prompts!")

if __name__ == '__main__':
    seed_tags()
