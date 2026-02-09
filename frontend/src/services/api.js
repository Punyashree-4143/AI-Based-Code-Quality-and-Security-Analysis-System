import axios from "axios";

// Backend base URL from environment (Vite + Vercel)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const reviewCode = async (payload) => {
  const response = await axios.post(
    `${API_BASE_URL}/api/v1/review`,
    payload,
    {
      headers: {
        "Content-Type": "application/json"
      }
    }
  );

  return response.data;
};
