# My Quiz Answers

#### How long did you spend on the coding test below?

>I spend a good bit of time mapping my approach to the concepts of the different frame works I used. After following my experience with modeling boilerplate and implementing base ideas, relating and directing data became quick and simple to do.

#### What would you add to your solution if you had more time?

>With more time, I would have liked to implement an image upload and the meta data input. I code backend support for it, but didn't create a Vue for it. I would have made the Vue dynamically apply new key values to an object that would be JSON stringified and saved as the raw meta raw value.

#### What was the most useful feature that was added to the latest version of your chosen language?

>I really like the usage of object destructing in ECMAScript implementations. Making all of the property values referenced available as variables makes for simple syntax and very readable code.

#### Please include a snippet of code that shows how you've used it.

```
const makeObj = (data) => {
  return {
    "someValue": data,
    "hello": [0, 1, 2, 'world']
  }
};

let { someValue, hello } = makeObj("hello");

console.log(someValue, hello);
//Result: hello [0, 1, 2, 'world']
```

#### How would you track down a performance issue in production? Have you ever had to do this?

>My process to resolving issues in production is to first test the route, or interface component live, try to recreate the results to narrow down where the problem may lay. Next I like to go over any newly committed changes to find any possibly unkept code. If nothing sticks out in commits, making an offline clone and partial database is my best bet to capture the source of a bug. I've correct production issues, and feature requests on a company proprietary client portal, making changes to the user interface source code, as well as server scripting to cover the customer use cases.
