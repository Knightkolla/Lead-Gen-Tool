import React, { useState } from 'react'
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material'

interface SearchParams {
  companyName: string
  industry: string
  location: string
  minEmployees: string
  maxEmployees: string
}

interface Company {
  name: string
  industry: string
  location: string
  employeeCount: number
  revenue: string
  website: string
}

const LeadEnrichmentApp: React.FC = () => {
  const [searchParams, setSearchParams] = useState<SearchParams>({
    companyName: '',
    industry: '',
    location: '',
    minEmployees: '',
    maxEmployees: '',
  })

  const [searchResults, setSearchResults] = useState<Company[]>([])

  const handleSearch = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchParams),
      })

      if (!response.ok) {
        throw new Error('Search failed')
      }

      const data = await response.json()
      setSearchResults(data)
    } catch (error) {
      console.error('Error searching companies:', error)
    }
  }

  const handleInputChange = (field: keyof SearchParams) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setSearchParams((prev) => ({
      ...prev,
      [field]: event.target.value,
    }))
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Company Search
          </Typography>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                  <TextField
            label="Company Name"
            value={searchParams.companyName}
            onChange={handleInputChange('companyName')}
            size="small"
                  />
                  <TextField
            label="Industry"
            value={searchParams.industry}
            onChange={handleInputChange('industry')}
            size="small"
                  />
                  <TextField
            label="Location"
            value={searchParams.location}
            onChange={handleInputChange('location')}
            size="small"
                  />
                  <TextField
            label="Min Employees"
                    type="number"
            value={searchParams.minEmployees}
            onChange={handleInputChange('minEmployees')}
            size="small"
                  />
                  <TextField
            label="Max Employees"
            type="number"
            value={searchParams.maxEmployees}
            onChange={handleInputChange('maxEmployees')}
            size="small"
                  />
          <Button variant="contained" onClick={handleSearch}>
            Search
          </Button>
            </Box>
          </Paper>

      {searchResults.length > 0 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Company Name</TableCell>
                <TableCell>Industry</TableCell>
                <TableCell>Location</TableCell>
                <TableCell>Employee Count</TableCell>
                <TableCell>Revenue</TableCell>
                <TableCell>Website</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {searchResults.map((company, index) => (
                <TableRow key={index}>
                  <TableCell>{company.name}</TableCell>
                  <TableCell>{company.industry}</TableCell>
                  <TableCell>{company.location}</TableCell>
                  <TableCell>{company.employeeCount}</TableCell>
                  <TableCell>{company.revenue}</TableCell>
                  <TableCell>
                    <a href={company.website} target="_blank" rel="noopener noreferrer">
                      {company.website}
                    </a>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
          )}
        </Box>
  )
}

export default LeadEnrichmentApp
