import api from "../api/axios";

export const scanPrompt = async (prompt, projectId) => {
  const response = await api.post("/prompt-scan", {
    prompt,
    project_id: projectId
  });
  return response.data;
};