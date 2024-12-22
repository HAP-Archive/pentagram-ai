import { NextResponse } from "next/server";
import { promises as fs } from "fs";
import crypto from "crypto";
import path from "path";

const MODAL_URL = process.env.DEPLOYED_MODAL_URL;

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { prompt } = body;

    if (!prompt) {
      return NextResponse.json({ success: false, error: "Prompt is required." }, { status: 400 });
    }

    const url = new URL(MODAL_URL as string);
    url.searchParams.append("prompt", prompt);

    const response = await fetch(url.toString(), {
      method: "GET",
      headers: { "Accept": "application/json" },
    });

    if (response.status !== 200) {
      throw new Error(`Modal returned status ${response.status}`);
    }

    // Generate image buffer
    const imageBuffer = await response.arrayBuffer();

    // Generate unique filename and path
    const fileName = `${crypto.randomUUID()}.jpeg`;
    const publicImgPath = path.join(process.cwd(), "public", "img");
    const filePath = path.join(publicImgPath, fileName);

    // Ensure the "public/img" directory exists
    await fs.mkdir(publicImgPath, { recursive: true });

    // Save the image
    await fs.writeFile(filePath, Buffer.from(imageBuffer));

    return NextResponse.json({
      success: true,
      imageUrl: `/img/${fileName}`, // Static path to the image
    });
  } catch (error: any) {
    console.error(error);
    return NextResponse.json({
      success: false,
      error: error.message || "An unexpected error occurred.",
    });
  }
}
