"use client";

import TiltCard from "@/components/ui/tilt-card";
import { useState } from "react";

export default function Home() {
  const [userPrompt, setUserPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const [title, setTitle] = useState("");
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [content, setContent] = useState("");
  const [hashtags, setHashtags] = useState<string[]>([]);

  const generateImage = async () => {
    try {
      const response = await fetch("/api/generate-image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: userPrompt }),
      });
  
      const data = await response.json();
  
      if (!data.success) {
        throw new Error(data.error || "Failed to generate image.");
      }
  
      if (data.imageUrl) {
        setImageUrl(data.imageUrl);
      }

    } catch (error: unknown) {
      if (error instanceof Error) {
        console.error(`Some error occurred: ${error.message}`);
      }
    }
  };

  const generateVito = async () => {
    try {
      const response = await fetch(`/api/generate-vito`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        }, 
        body: JSON.stringify({ 
          prompt: userPrompt,
          max_completion_tokens: 256,
          temperature: 1,
          top_p: 1,
          seed: Math.floor(Math.random() * 1000).toString()
         }),
      });

      if (!response.ok) {
        const errorMessage = `Received error ${response.status} from vito`;
        console.error(errorMessage);

        throw new Error(`HTTP error! Status code: ${response.status}, message: ${errorMessage}`)
      }

      const result = await response.json();

      if (result.success && result.data) {
        setTitle(result.data.title);
        setContent(result.data.content);
        
        const processHashtags = result.data.hashtags.map((tag: any) => (typeof tag === 'string' ? tag : tag.tag));
        setHashtags(processHashtags);
      }

    } catch (error) {
      if (error instanceof Error) {
        console.error(`Some error occurred: ${error.message}`);
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (!userPrompt) {
        throw new Error(`Prompt provided: ${userPrompt}. This is invalid and a prompt is required.`);
      }

      await Promise.all([
        generateImage(),
        generateVito()
      ]);

    } catch (error) {
      if (error instanceof Error) {
        console.error(`Some error occurred: ${error.message}`);
      }
      return;

    } finally {
      setIsLoading(false);

    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-between bg-[#121214] p-8">
      <main className="flex flex-col items-center justify-center w-full max-w-2xl">
        {imageUrl ? (
          <TiltCard
            title={title || "N/A"}
            imageUrl={imageUrl}
            content={content || "N/A"}
            hashtags={hashtags?.length > 0 ? hashtags : ["XXXX", "XXXX", "XXXX"]}
            className="mb-8"
          />
        ) : (
          <TiltCard
            title={title || "N/A"}
            imageUrl="img/714bc44c-66e2-4969-8410-32142ede2fa3.jpeg"
            content={content || "N/A"}
            hashtags={hashtags?.length > 0 ? hashtags : ["XXXX", "XXXX", "XXXX"]}
            className="mb-8"
          />
        )}
      </main>

      <footer className="w-full max-w-3xl mt-8">
        <form onSubmit={handleSubmit} className="w-full">
          <div className="flex flex-col sm:flex-row gap-4 items-stretch">
            <input
              type="text"
              value={userPrompt}
              onChange={(e) => setUserPrompt(e.target.value)}
              className="flex-1 p-4 rounded-md bg-slate-800 text-white placeholder-gray-400 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500 transition-all disabled:opacity-50"
              placeholder="Describe the image you are looking to generate..."
              disabled={isLoading}
            />

            <button
              type="submit"
              disabled={isLoading}
              className="rounded-md bg-gradient-to-tr from-slate-700 to-slate-600 py-3 px-6 text-center text-sm text-white shadow-md hover:shadow-lg hover:from-slate-800 hover:to-slate-700 active:shadow-none focus:bg-slate-700 focus:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none transition-all"
            >
              {isLoading ? "Generating..." : "Generate"}
            </button>

            <button
              type="button"
              disabled={isLoading}
              onClick={() => {
                setUserPrompt("");
                setTitle("");
                setImageUrl(null);
                setContent("");
                setHashtags([]);
              }}
              className="rounded-md bg-gradient-to-tr from-slate-600 to-slate-500 py-3 px-6 text-center text-sm text-white shadow-md hover:shadow-lg hover:from-slate-700 hover:to-slate-600 active:shadow-none focus:bg-slate-600 focus:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none transition-all"
            >
              {isLoading ? "Clearing..." : "Clear"}
            </button>
          </div>
        </form>
      </footer>
    </div>
  );
}
