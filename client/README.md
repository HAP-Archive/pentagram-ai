# Pentagram AI

Its like Instagram, but with a side dish of AI generated images using textual prompts and stable diffusion.

## Getting Started

### Prerequisites

There are a few things you must have installed before you can get started with this project,
namely but not limited to the following:
1. [Node.js](https://nodejs.org/en/download/)
2. [Git](https://git-scm.com/downloads)
3. [GitHub CLI](https://cli.github.com/)
4. [Docker](https://docs.docker.com/get-docker/)
5. [Python](https://www.python.org/downloads/)


## Installation & Setup 

The first thing you need to do is clone the repository, which can be done using the following command:
```bash
git clone https://github.com/HAP-Archive/pentagram-ai.git .
```

Navigate to the project directory for the `client` and `server` folders:
```bash
cd ./client/
```

In another terminal, navigate to the `server` folder and install the dependencies:
```bash
cd ../server/
pip install -r requirements.txt
```

> [!NOTE]
> The server folder will be using python coupled with Flask, and will also 
> include a `Dockerfile` to build the image (if you want to run it locally).
> Alongside this, we will be using Cerebras for AI inference and Stable Diffusion 
> models for image generation.



Then, navigate to the project directory:
```bash
cd pentagram
```

Then, install the dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Tasks

- Take a look at the TODOs in the repo, namely:

    - `src/app/page.tsx`: This is where the user can input their prompt and generate an image. Make sure to update the UI and handle the API response to display the images generated

    - `src/app/api/generate-image/route.ts`: This is where the image generation API is implemented. Make sure to call your image generation API from Modal here


## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.
