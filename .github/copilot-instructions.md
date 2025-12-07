# Basirat - AI Coding Agent Instructions

## Project Overview
Basirat is a Django-based learning management system (LMS) for Uzbekistan with phone-based authentication, multi-language support (Uzbek, Russian, English), and sequential lesson progression tracking.

## Architecture & Key Patterns

### Authentication System
- **Custom user model**: `users.CustomUser` uses `phone_number` (not username/email) as `USERNAME_FIELD`
- Phone numbers validated via `phonenumber_field` with `PHONENUMBER_DEFAULT_REGION = 'UZ'`
- Custom manager in `users/managers.py` handles phone-based user creation
- Login/logout flows in `users/views.py` use phone authentication forms

### Course Hierarchy
```
Course (is_published flag)
  └─ Lesson (sequential via order field)
      └─ Material (learning resources OR task questions)
```

**Critical business logic:**
- Students must complete lessons sequentially: `Lesson.is_available_for(user)` checks all previous lessons completed
- Material completion tracked via `MaterialCompletion` model (unique_together on material + student)
- Enrollment requires admin approval: `Enrollment.STATUS_PENDING → ACCEPTED/REJECTED`

### Material Types (Dual-Purpose Model)
Materials serve two distinct roles enforced in `Material.clean()`:
- **Learning resources** (`material_type='learning'`): Require `content` or `media_file`, no question metadata
- **Task questions** (`material_type='task'`): Require `question_type` + `question_payload`, no media files

### Internationalization (i18n)
- **django-modeltranslation**: Enabled but `translation.py` is empty (configure per model as needed)
- Language codes: `uz` (default), `en`, `ru` - set via `MODELTRANSLATION_DEFAULT_LANGUAGE`
- All user-facing strings use `gettext_lazy` (`_()`) for translation
- Translation files in `locale/{uz,ru}/LC_MESSAGES/django.po`
- Time zone: `Asia/Tashkent`

### Settings Architecture
Multi-environment settings split in `application/settings/`:
- `defaults.py`: Base configuration with `.env` loading via `python-dotenv`
- `local.py`: Development overrides (SQLite, `DEBUG=True`, local paths)
- `production.py`: Production-specific settings
- Import pattern: `--settings=application.settings.local` (used in Docker start scripts)

### Permission System
Custom decorators in `users/decorators.py`:
- `@student_required`: Check `user.is_student == True`
- `@admin_required`: Check `user.is_student == False` (admins have `is_student=False`)

## Development Workflows

### Running Locally (Docker)
```bash
docker-compose -f docker-compose.local.yml up
```
- Postgres DB (port not exposed externally)
- Django on `0.0.0.0:8010` (mapped to host `8011`)
- Entrypoint waits for Postgres, runs migrations, creates superuser if none exists

### Running Without Docker
```bash
python manage.py migrate --settings=application.settings.local
python manage.py createsuperuserifnone --settings=application.settings.local
python manage.py runserver --settings=application.settings.local
```

### Database Migrations
Always specify settings module:
```bash
python manage.py makemigrations --settings=application.settings.local
python manage.py migrate --settings=application.settings.local
```

### Translation Updates
After modifying translatable strings:
```bash
python manage.py makemessages -l uz -l ru
# Edit locale/*/LC_MESSAGES/django.po files
python manage.py compilemessages
```

## Django Admin Customizations

### Enrollment Management
- Bulk actions in `EnrollmentAdmin`: "Mark selected as accepted/rejected"
- Actions call `queryset.update()` with `answered_at=timezone.now()`
- Search by `student__phone_number` (custom user field)

### Inline Editing
- `CourseAdmin`: Shows inline `LessonInline` + `EnrollmentInline`
- `LessonAdmin`: Shows inline `MaterialInline` with stacked layout
- Auto-prepopulated slugs from `title` field

## API Documentation
- **drf-spectacular** configured for OpenAPI schema generation
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- Schema endpoint: `/api/schema/`

## File Upload Conventions
- Media files uploaded to `media/materials/%Y/%m/%d/` (date-based paths)
- `MEDIA_URL = '/media/'` served via `static()` helper in URLs (dev only)
- Production uses Nginx to serve media (see `compose/production/nginx/`)

## Common Pitfalls

1. **Material validation**: Mixing learning/task fields violates `Material.clean()` - will raise `ValidationError`
2. **Sequential lesson access**: Always check `lesson.is_available_for(user)` before rendering lesson content
3. **Enrollment status**: Students can only access lessons if `Enrollment.status == 'accepted'`
4. **Phone number format**: Use international format `+998901234567` for Uzbek numbers
5. **Settings module**: Never run Django commands without `--settings=application.settings.{local|production}`

## Code Style Patterns

- Models use `verbose_name` with `gettext_lazy` for all fields
- Related names follow plural convention: `course.lessons`, `lesson.materials`
- Ordering defined in `Meta.ordering` (avoid runtime `.order_by()` calls)
- Admin actions update via `queryset.update()` for bulk efficiency
- View permissions enforced via decorators + enrollment checks, not middleware

## Testing Strategy
- Test files exist (`tests.py`) but are currently empty - add tests for:
  - Sequential lesson progression logic
  - Material type validation
  - Enrollment status transitions
  - Phone-based authentication flows
