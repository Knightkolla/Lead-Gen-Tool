import axios from 'axios';
import { API_BASE_URL } from '../config';

export const fetchAnalytics = async () => {
  const response = await axios.get(`${API_BASE_URL}/api/analytics`);
  return response.data;
};

export const fetchLeads = async () => {
  const response = await axios.get(`${API_BASE_URL}/api/leads`);
  return response.data;
};

export const fetchLeadById = async (id: string) => {
  const response = await axios.get(`${API_BASE_URL}/api/leads/${id}`);
  return response.data;
};

export const createLead = async (lead: any) => {
  const response = await axios.post(`${API_BASE_URL}/api/leads`, lead);
  return response.data;
};

export const updateLead = async (id: string, lead: any) => {
  const response = await axios.put(`${API_BASE_URL}/api/leads/${id}`, lead);
  return response.data;
};

export const deleteLead = async (id: string) => {
  const response = await axios.delete(`${API_BASE_URL}/api/leads/${id}`);
  return response.data;
};

export const searchLeads = async (query: string) => {
  const response = await axios.get(`${API_BASE_URL}/api/leads/search?q=${encodeURIComponent(query)}`);
  return response.data;
}; 