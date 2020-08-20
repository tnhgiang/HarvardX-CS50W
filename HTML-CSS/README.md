# HTML and CSS
**HTML**: is a language that we can use to describe the structure of the web page.

**CSS**: is a language that we can use to describe the style of the web page.

**Responsive Design**: Responsive design is all about making sure that our web pages look good regardless of how you're looking at the web page (eg: no matter you're using computer, mobile phone or tablet).

**Bootstrap**: was a very popular CSS library that we can use to use some styling that we don't have to write from the scratch.

**Sass**: is a language that is essentially an extension to CSS. It help us use and manipulate CSS in a faster way and remove some of the repetition. Adding variables to our CSS code is one of the very powerful features that Sass give us to factor out commonalities.

The advantages of separating ```*.css``` to another file:
* No need to duplicate the same code in many places where declare the style of element.
* Make the code more readable and well organized.
* To be reuseable, *.css files can use in many html pages having the same style information.

Note:
* Copying a lot of the same information from one place to another is probably not the best design. So, you should start to think about how might you design this a little bit better.

Some common ```HTML Tag```:
* head: Not be seen by a user, but be useful information for web browser.
* div: be a division of the page, some section of the page that's going to have some content inside of it. Use div bacause it makes it easy to reference a particular div or nest information inside of other pieces of information, or just to devide and break up our page into multiple different sections.

Some useful ```CSS properties```:
* padding: The padding on the inside of the element.
* margin: Add some margin along the outside of the border.
* border: Add some sort of border around HTML elements.
* font-family: Specify what font used in order to display a text.
* font-size: Specify the size of a text.
* font-weight: Specify whether using normal text or bolded text.

```IDs``` and ```Class```:
* ```IDs``` are the way of giving a name to an HTML element that is unique.

```html
<head>
    <style>
        #foo {
            color: blue;
        }
    </style>
</head>
<body>
    <h1 id="foo"> Heading 1</h1>
</body>
```

* ```Class``` is a way of giving a name to and HTML element that might not be unique. It might apply it to zero, one, two or multiple different HTML elements.

```html
<head>
    <style>
        .baz {
            color: blue;
        }
    </style>
</head>
<body>
    <h1 class="baz"> Heading 1</h1>
</body>
```

The order of ```CSS selector``` specificity:
1. inline
2. id
3. class
4. type

Components of the responsive design:
1. Viewpoint: this is the entire area of the web page that displays content to the user. We do need to make the web page adapt to different sized screens.
2. Media queries: these are all about controlling how our web page is going to look depending on how we render that particular page or what size of the screen that we're rendering that page on.
3. Flexbox: this is quite helpful if we have multiple elements displaying on the same page at the same time that might be overflow.
4. Grids: this is to arrange things in a particular grid.

Using ```Sass``` in 2-step:
1. Write Sass code, compile it into CSS (because Chrome or Safari doesn't understand *.scss).

    ```scss
    // Use $ notation to declare a variable
    $color: red
    ```

    Nested CSS selectors:

    ```scss
    div {
        font-size: 18px;

        p {
            color: blue;
        }

        ul {
            color: green;
        }
    }
    ```

    Inheritance:

    ```scss
    %message {
        font-size: 18px;
        font-weight: bold;
    }

    .success {
        @extend %message
        background-color: green;
    }
    ```

    Compilation: 

    ```bash
    # Excute the compilation
    sass variable.scss:variable.css
    # sass will recompile the css file whenever the corresponding css file has changes
    sass --watch variable.scss:variable.css
    ```

2. Link the CSS to the particular page.

    ```html
    <link rel="stylesheet" href="variable.css">
    ```