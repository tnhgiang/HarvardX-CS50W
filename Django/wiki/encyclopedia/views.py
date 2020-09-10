import os
import markdown2
import random
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label='Title')
    content = forms.CharField(label='Mardown', widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def open(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, 'encyclopedia/error.html', {
            'title': title
        })

    entry = markdown2.markdown(entry)
    return render(request, 'encyclopedia/open.html', {
            'entry': entry,
            'title': title
        })


def search(request):
    if request.method == "POST":
        entry_title = request.POST['q']

        # Server-side validation
        if isinstance(entry_title, str):
            list_entries = util.list_entries()

            if entry_title in list_entries:
                return HttpResponseRedirect(
                        reverse(
                                "encyclopedia:open",
                                kwargs={'title': entry_title}
                            )
                    )
            else:
                entries = []

                for idx in range(len(list_entries)):
                    if entry_title in list_entries[idx]:
                        entries.append(list_entries[idx])

                return render(request, 'encyclopedia/search.html', {
                    'entries': entries,
                    'entry_title': entry_title
                })


def new(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)

        # Server-sida validation
        if form.is_valid():
            entry_title = form.cleaned_data['title']

            # Check whether title already exists or not
            if entry_title not in util.list_entries():
                file_name = entry_title + '.md'
                content = form.cleaned_data['content']

                # Save entry to disk
                default_storage.save(os.path.join(
                    'entries', file_name), ContentFile(content))

                return HttpResponseRedirect(
                    reverse(
                        'encyclopedia:open',
                        kwargs={'title': entry_title}
                    )
                )
            else:
                form.errors.update(
                        {'title': ['Error: The encyclopedia already exists!']}
                    )

        return render(request, 'encyclopedia/new.html', {
            'form': form
        })
    else:
        return render(request, 'encyclopedia/new.html', {
            'form': NewPageForm()
        })


def edit(request, title):
    if request.method == 'POST':
        form = NewPageForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']

            file_name = title + '.md'
            # Remove the old file
            default_storage.delete(
                os.path.join('entries', file_name)
            )
            # Save the new file to disk
            default_storage.save(os.path.join(
                    'entries', file_name), ContentFile(content))

            return HttpResponseRedirect(
                reverse(
                    'encyclopedia:open',
                    kwargs={'title': title}
                )
            )
        else:
            render(request, 'encyclopedia/edit.html', {
                'form': form
            })
    else:
        # Load entry from disk
        file_name = title + '.md'
        content = default_storage.open(
                os.path.join('entries', file_name)
            ).read().decode('utf-8')

        entry = {
            'title': title,
            'content': content
        }
        form = NewPageForm(entry)

        # Set the title filed is readonly
        form.fields['title'].widget.attrs['readonly'] = True

        return render(request, 'encyclopedia/edit.html', {
            'form': form
        })


def random_page(request):
    list_entries = util.list_entries()

    index = random.randint(0, len(list_entries) - 1)

    return HttpResponseRedirect(
        reverse(
            'encyclopedia:open',
            kwargs={'title': list_entries[index]}
        )
    )
