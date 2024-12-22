"use client";

import { motion } from "framer-motion";
import { useState, useCallback, MouseEvent } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface TiltCardProps {
  title: string;
  imageUrl: string;
  content: string;
  hashtags: string[];
  className?: string;
}

export default function TiltCard({
  title,
  imageUrl,
  content,
  hashtags,
  className,
}: TiltCardProps) {
  const [rotate, setRotate] = useState({ x: 0, y: 0 });

  const handleMouseMove = useCallback((e: MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((y - centerY) / centerY) * 10;
    const rotateY = ((centerX - x) / centerX) * 10;
    setRotate({ x: rotateX, y: rotateY });
  }, []);

  const handleMouseLeave = () => {
    setRotate({ x: 0, y: 0 });
  };

  const calculatePostReadTime = (content: string) => {
    const WPM = 256;
    const words = content.split(/\s+/).length;
    const minutes = Math.round(words / WPM);
    return `${minutes}m read time`;
  }

  return (
    <motion.div
      className={`relative group ${className}`}
      style={{ perspective: 1000 }}
    >
      <motion.div
        className="w-full h-full"
        style={{
          transform: `rotateX(${rotate.x}deg) rotateY(${rotate.y}deg)`,
          transformOrigin: "center center",
        }}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        transition={{
          stiffness: 300,
          damping: 30,
          type: "spring",
        }}
      >
        <Card
          className={cn(
            "relative shadow-xl bg-transparent border rounded-lg overflow-hidden transition-transform group-hover:scale-105 group-hover:shadow-lg"
          )}
        >
          <CardHeader className="flex flex-row items-center gap-4 p-4 bg-transparent">
            <CardTitle className="text-slate-400 text-lg font-serif">
                {title}
            </CardTitle>
          </CardHeader>

          <CardContent className="px-4 py-4 flex text-slate-400 text-md text-wrap font-serif">
            {content} 
          </CardContent>

          <div className="px-4 py-2 text-gray-400">
            <span className="text-gray-400 text-sm font-serif">
              {new Date().toLocaleDateString()} • {content.length} chars • {calculatePostReadTime(content)}
            </span>
          </div>

          <div className="w-full overflow-hidden rounded-lg mt-4 px-4">
            <motion.img
              src={imageUrl}
              width={400}
              height={400}
              className="w-[400px] h-[300px] object-cover object-center rounded-lg"
              whileHover={{
                transition: {
                  duration: 0.5,
                  ease: "easeInOut",
                },
              }}
            />
          </div>
          <br/>
          <div className="flex flex-wrap gap-2 px-4 text-sm">
            {hashtags.map((hashtag, index) => (
              <span
                key={index}
                className="inline-flex items-center rounded-md bg-transparent px-2 py-1 text-md font-medium font-serif text-slate-400 ring-1 ring-inset ring-slate-400 transition-colors"
              >
                {hashtag}
              </span>
            ))}
          </div>
          <br/>
        </Card>
      </motion.div>
    </motion.div>
  );
}
