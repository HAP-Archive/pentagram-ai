import { NextResponse } from "next/server";

const VITO_URL = "http://localhost:8000/api/v1/inference";

// ANCHOR: What does Vito stand for? Viral Instagram Text Output
export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { prompt, max_completion_tokens, temperature, top_p, seed } = body;

        const url = new URL(VITO_URL);
        url.searchParams.append("prompt", prompt);
        url.searchParams.append("max_completion_tokens", max_completion_tokens.toString());
        url.searchParams.append("temperature", temperature.toString());
        url.searchParams.append("top_p", top_p.toString());
        url.searchParams.append("seed", seed.toString());

        console.log(`Request to vito: ${url.toString()}`);

        const response = await fetch(url.toString(), {
            method: "POST",
            headers: {
                "Accept": "application/json",
            },
        });

        if (!response.ok) {
            const errorMessage = `Received error ${response.status} from vito`;
            console.error(errorMessage);

            throw new Error(`HTTP error! Status code: ${response.status}, message: ${errorMessage}`)
        }

        const data = await response.json();
        return NextResponse.json({
            success: true,
            data,
        });

    } catch (error) {
        if (error instanceof Error) {
            return NextResponse.json({
                success: false,
                error: `Something went wrong, recieved error ${error.message}`
            });
        }
    }
}