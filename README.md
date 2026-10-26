# Crystal pilot

A small, dependency-free Node.js project for trying managed Claude with Crystal.
The root manifest lets Crystal's cloud build planner recognize the project.

## Try it with Crystal

1. Clone this repository into a new folder and choose it in Crystal's **First session** step.
2. Choose **Copy test prompt**, then **Open in Terminal**. Paste the prompt into Claude.
3. Let Claude finish, exit normally, and choose **Check result** in Crystal.

Keep the generated test file unchanged until the result check finishes. A successful
test verifies the returned file and the session evidence for your own account.

Crystal supplies the remote runtime; Node.js does not need to be installed on your Mac.

## Develop the sample

With Node.js 22, run:

```sh
npm ci
npm run build
npm start
```

The sample uses only Node.js built-ins and makes no network requests.

Test line.
