# Requirements for this Project

For this project, we are tasked with building an instagram clone, where instead of users uploading pitcutres themselves, they can generate images
with text prompts. Instead of using an existing image generation API, we will be hosting an image generation model on serverless GPUs to ensure
a high level of preormence and smooth user experience.

**Project Requirements:**
Stage 1 Requirements:
- Host a image generation model (Stable Diffusion or Dall-E) on a serverless GPU through Modal, ensuring low-latency, high-throughput, and smooht user experience.
- Create a web app that allows users to generate images from text prompts, manage their creations amd intereact socially through likes, comments, and shares.
- Incoporate intuitive UI/UX design, authentication, and efficient image management with prompt history and search features.
  
Stage 2 Requirements:
- Build a recommendation engine that suggests images based on the preference and existing feed of users, balance both new content discovery and user preference.
- Add the ability to search for images based on tags, filters, and other parameters (semantic search).
- Implement a user-friendly interface for image sharing and discovery.
- Integrate a messaging system with sockets to enable real-time chatting between platform users.
- Prevent harmful content or inappropriate content from being generated.
- Manage the dynamic scaling of GPU resources to handle more demanding workloads and traffic without exceeding cost or causing performance bottlenecks.

**Project Deliverables:**
- Deployed Stable Diffusion or Dall-E model on a serverless GPU through Modal.
- Web application that allows users to generate images from text prompts, with a user-friendly interface and intuitive UI/UX design.
- Video demonstration of the application in action and how it works from the inside out.
- Detailed documentation of the project, including the architecture, design, and implementation details.
