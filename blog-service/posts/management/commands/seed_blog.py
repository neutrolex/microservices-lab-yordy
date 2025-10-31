from django.core.management.base import BaseCommand
from django.utils import timezone
from categories.models import Category
from authors.models import Author
from posts.models import Post
import random


class Command(BaseCommand):
    help = 'Seed blog data with categories, authors and posts'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding blog data...')

        # Crear categorías
        categories_data = [
            'Technology',
            'Programming',
            'Web Development',
            'Data Science',
            'DevOps'
        ]

        categories = []
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'is_active': True}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'✅ Created category: {cat_name}')

        # Crear autores
        authors_data = [
            {'display_name': 'John Doe', 'email': 'john@blog.com'},
            {'display_name': 'Jane Smith', 'email': 'jane@blog.com'},
            {'display_name': 'Mike Johnson', 'email': 'mike@blog.com'},
        ]

        authors = []
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                email=author_data['email'],
                defaults={'display_name': author_data['display_name']}
            )
            authors.append(author)
            if created:
                self.stdout.write(f'✅ Created author: {author_data["display_name"]}')

        # Crear posts
        posts_data = [
            {
                'title': 'Getting Started with Django REST Framework',
                'body': 'Django REST Framework is a powerful toolkit for building Web APIs. In this comprehensive guide, we will explore how to create robust APIs using DRF. We will cover serializers, viewsets, authentication, and much more. This tutorial is perfect for developers who want to build scalable web applications.',
                'status': 'published'
            },
            {
                'title': 'Understanding Docker Containers',
                'body': 'Docker has revolutionized the way we deploy applications. Containers provide a lightweight, portable way to package applications with all their dependencies. In this article, we will dive deep into Docker concepts, including images, containers, volumes, and networking.',
                'status': 'published'
            },
            {
                'title': 'Python Best Practices for 2024',
                'body': 'Python continues to be one of the most popular programming languages. In this post, we will discuss the latest best practices for writing clean, maintainable Python code. Topics include type hints, async programming, testing strategies, and performance optimization.',
                'status': 'published'
            },
            {
                'title': 'Introduction to Machine Learning',
                'body': 'Machine Learning is transforming industries across the globe. This beginner-friendly guide will introduce you to the fundamental concepts of ML, including supervised learning, unsupervised learning, and neural networks. We will also explore popular libraries like scikit-learn and TensorFlow.',
                'status': 'published'
            },
            {
                'title': 'Building Microservices with FastAPI',
                'body': 'FastAPI is a modern, fast web framework for building APIs with Python. In this tutorial, we will learn how to create microservices using FastAPI, including automatic API documentation, dependency injection, and async support.',
                'status': 'published'
            },
            {
                'title': 'Redis Caching Strategies',
                'body': 'Redis is an in-memory data structure store that can be used as a database, cache, and message broker. This article explores different caching strategies and patterns when using Redis in production applications.',
                'status': 'published'
            },
            {
                'title': 'PostgreSQL Performance Tuning',
                'body': 'PostgreSQL is a powerful relational database system. Learn how to optimize your PostgreSQL database for better performance, including indexing strategies, query optimization, and configuration tuning.',
                'status': 'published'
            },
            {
                'title': 'JWT Authentication in Web Applications',
                'body': 'JSON Web Tokens (JWT) provide a secure way to transmit information between parties. This guide covers how to implement JWT authentication in web applications, including token generation, validation, and best security practices.',
                'status': 'published'
            },
            {
                'title': 'CSS Grid vs Flexbox: When to Use Each',
                'body': 'CSS Grid and Flexbox are powerful layout systems in CSS. This article compares both approaches and provides guidance on when to use each one for different layout scenarios.',
                'status': 'published'
            },
            {
                'title': 'Testing Strategies for Django Applications',
                'body': 'Testing is crucial for maintaining code quality. Learn about different testing strategies for Django applications, including unit tests, integration tests, and test-driven development practices.',
                'status': 'published'
            },
            # Draft posts
            {
                'title': 'Advanced React Patterns (Draft)',
                'body': 'This is a draft post about advanced React patterns including render props, higher-order components, and custom hooks.',
                'status': 'draft'
            },
            {
                'title': 'Kubernetes Deployment Guide (Draft)',
                'body': 'A comprehensive guide to deploying applications on Kubernetes. This draft covers pods, services, deployments, and ingress controllers.',
                'status': 'draft'
            },
        ]

        # Crear posts con datos aleatorios
        for i, post_data in enumerate(posts_data):
            author = random.choice(authors)
            category = random.choice(categories)
            
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'body': post_data['body'],
                    'author': author,
                    'category': category,
                    'status': post_data['status'],
                    'views': random.randint(0, 1000),
                }
            )
            
            if created:
                self.stdout.write(f'✅ Created post: {post_data["title"]}')

        # Crear posts adicionales para llegar a 30
        additional_titles = [
            'API Design Best Practices',
            'Monitoring Applications with Prometheus',
            'GraphQL vs REST APIs',
            'Securing Web Applications',
            'Database Migration Strategies',
            'Cloud Computing Fundamentals',
            'Agile Development Methodologies',
            'Code Review Best Practices',
            'Continuous Integration with GitHub Actions',
            'Performance Optimization Techniques',
            'Mobile App Development Trends',
            'Blockchain Technology Explained',
            'Artificial Intelligence in Healthcare',
            'Cybersecurity Fundamentals',
            'Open Source Contribution Guide',
            'Remote Work Best Practices',
            'Project Management Tools',
            'Version Control with Git',
        ]

        for title in additional_titles:
            if Post.objects.filter(title=title).exists():
                continue
                
            author = random.choice(authors)
            category = random.choice(categories)
            status = random.choice(['published', 'published', 'published', 'draft'])  # 75% published
            
            Post.objects.create(
                title=title,
                body=f'This is the content for {title}. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
                author=author,
                category=category,
                status=status,
                views=random.randint(0, 500),
            )
            self.stdout.write(f'✅ Created additional post: {title}')

        # Estadísticas finales
        total_categories = Category.objects.count()
        total_authors = Author.objects.count()
        total_posts = Post.objects.count()
        published_posts = Post.objects.filter(status='published').count()
        draft_posts = Post.objects.filter(status='draft').count()

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Seeding completed!\n'
                f'📁 Categories: {total_categories}\n'
                f'👥 Authors: {total_authors}\n'
                f'📝 Total Posts: {total_posts}\n'
                f'📰 Published: {published_posts}\n'
                f'📄 Drafts: {draft_posts}'
            )
        )