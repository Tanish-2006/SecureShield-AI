import api from "../api/axios";

export const getThreatLogs = async (projectId) => {
  const response = await api.get(`/threat-logs/${projectId}`);
  return response.data;
};