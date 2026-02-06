import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

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
