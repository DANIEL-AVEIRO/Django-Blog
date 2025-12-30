from django.shortcuts import render, redirect
from myapp.models import CategoryModel, PostModel, CommentModel, NotificationModel
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings


def Index(request):
    search = request.GET.get("search")
    posts = PostModel.objects.filter(is_active=True).order_by("-created_at")
    if search:
        posts = posts.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(category__name__icontains=search)
        ).order_by("-created_at")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html", {"posts": page_obj})


@login_required(login_url="/login/")
def PostList(request):
    posts = PostModel.objects.all()
    return render(request, "post_list.html", {"posts": posts})


def PostDetail(request, pk):
    post = PostModel.objects.get(id=pk)
    comments = CommentModel.objects.filter(post_id=post.id).order_by("-created_at")
    return render(request, "post_detail.html", {"post": post, "comments": comments})


def PostCreate(request):
    categories = CategoryModel.objects.all().order_by("-created_at")
    if request.method == "GET":
        return render(request, "post_create.html", {"categories": categories})
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        category = request.POST.get("category")
        post = PostModel.objects.create(
            title=title, description=description, image=image, category_id=category
        )
        post.save()

        users = User.objects.all()

        subject = "New Post For You"
        message = f"Post title is {post.title}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email for user in users]
        send_mail(subject, message, email_from, recipient_list)

        notification = NotificationModel.objects.create(
            title=f"New post for you. title is {post.title}"
        )
        notification.save()
        return redirect("/post/list/")


def PostUpdate(request, pk):
    categories = CategoryModel.objects.all().order_by("-created_at")
    post = PostModel.objects.get(id=pk)
    if request.method == "GET":
        return render(
            request, "post_update.html", {"post": post, "categories": categories}
        )
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        # image =  new image
        # post.image = old image
        image = request.FILES.get("image")
        post.title = title
        post.description = description
        post.category_id = category
        if image:
            post.image.delete()
            post.image = image
        else:
            post.image = post.image
        post.save()
        return redirect("/post/list/")


def PostDelete(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == "GET":
        return render(request, "post_delete.html", {"post": post})
    if request.method == "POST":
        if post.image:
            post.image.delete()
        post.delete()
        return redirect("/post/list/")


# ============= POST DEACTIVATE / ACTIVATE =============
# GET METHOD


# def PostActivate(request, pk):
#     post = PostModel.objects.get(id=pk)
#     post.is_active = True
#     post.save()
#     messages.success(request, "Post is activate successfully")
#     return redirect("/post/list/")


# def PostDeactivate(request, pk):
#     post = PostModel.objects.get(id=pk)
#     post.is_active = False
#     post.save()
#     messages.success(request, "Post is deactivate successfully")
#     return redirect("/post/list/")


# POST METHOD


def PostActivate(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == "POST":
        post.is_active = True
        post.save()
        messages.success(request, "Post is activate successfully")
        return redirect("/post/list/")


def PostDeactivate(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == "POST":
        post.is_active = False
        post.save()
        messages.success(request, "Post is deactivate successfully")
        return redirect("/post/list/")


@permission_required("myapp.view_categorymodel", login_url="/login/")
def CategoryList(request):
    categories = CategoryModel.objects.all()
    return render(request, "category_list.html", {"categories": categories})


@permission_required("myapp.add_categorymodel", login_url="/login/")
def CategoryCreate(request):
    if request.method == "GET":
        return render(request, "category_create.html")
    if request.method == "POST":
        name = request.POST.get("name")
        category = CategoryModel.objects.create(name=name)
        category.save()
        return redirect("/category/list/")


def CategoryUpdate(request, pk):
    category = CategoryModel.objects.get(id=pk)
    if request.method == "GET":
        return render(request, "category_update.html", {"category": category})
    if request.method == "POST":
        name = request.POST.get("name")
        category.name = name
        category.save()
        return redirect("/category/list/")


def CategoryDelete(request, pk):
    category = CategoryModel.objects.get(id=pk)
    if request.method == "GET":
        return render(request, "category_delete.html", {"category": category})
    if request.method == "POST":
        category.delete()
        return redirect("/category/list/")


def Login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            messages.warning(request, "You are already login")
            return redirect("/")
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        # if user is not None:
        if user:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect("/")
        else:
            messages.error(request, "Login Failed")
            return redirect("/login/")


def Logout(request):
    logout(request)
    return redirect("/")


def CommentCreate(request, post_pk):
    if request.method == "POST":
        message = request.POST.get("message")
        post = PostModel.objects.get(id=post_pk)
        comment = CommentModel.objects.create(
            message=message, post_id=post.id, author_id=request.user.id
        )
        comment.save()

        notification = NotificationModel.objects.create(
            title=f"{comment.author.username} is comment on {comment.post.title}"
        )
        notification.save()
        messages.success(request, "Comment created successfully")
        return redirect(f"/post/detail/{post.id}/#comment-box")


def Register(request):
    if request.method == "GET":
        return render(request, "register.html")
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active = False
            
        )
        user.save()
        subject = "New Registration"
        message = f"Welcome New User {user.username}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list)
        # login(request, user)
        messages.success(request, f"Account was created for {user.username}")
        return redirect("/")


def ChangePassword(request):
    if request.method == "GET":
        return render(request, "change_password.html")
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")

        user = User.objects.get(id=request.user.id)

        if not user.check_password(old_password):
            messages.error(request, "Old password is wrong")
            return redirect("/change_password/")

        if old_password == new_password:
            messages.error(request, "Old password and new password should not be same")
            return redirect("/change_password/")

        if confirm_new_password != new_password:
            messages.error(request, "Password does not match")
            return redirect("/change_password/")

        user.set_password(new_password)
        user.save()
        return redirect("/")


def ReactionToggle(request, post_id):
    post = PostModel.objects.get(id=post_id)
    if not request.user in post.reaction.all():
        post.reaction.add(request.user)
        messages.success(request, "Liked")
    else:
        post.reaction.remove(request.user)
        messages.success(request, "Unliked")
    return redirect(f"/post/detail/{post.id}/")


def NotificationList(request):
    notifications = NotificationModel.objects.all()
    return render(request, "notifications.html", {"notifications": notifications})
