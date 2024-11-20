'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts'
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts'

interface ClusterData {
    gender: string
    body_shape: number
    cluster_id: number
    size_label: string
    centroid: number[]
    cluster_count: number
    sample_data: {
        Height_cm: number
        Weight: number
        "Bust/Chest": number
        Waist: number
        Hips: number
    }[]
    confidence_scores: {
        [key: string]: {
            S: number
            M: number
            L: number
            XL: number
        }
    }
}

export default function DetailedChartPage() {
    const [data, setData] = useState<ClusterData[]>([])
    const [selectedGender, setSelectedGender] = useState<string>('male')
    const [selectedBodyShape, setSelectedBodyShape] = useState<number>(1)
    const [loading, setloading] = useState(true);
    useEffect(() => {
        // In a real application, you would fetch this data from your API
        fetch('http://localhost:8000/size-chart/getalldetailedcharts')
            .then(response => response.json())
            .then(data => {
                setData(JSON.parse(data))
                console.log("coming data ",data)
                console.log(typeof data)
                setloading(false)
            })
    }, [])
    if (loading) {
        return <>loading</>
    }
    // console.log("data comes",data)
    const filteredData = data.filter(
        item => item.gender === selectedGender && item.body_shape === selectedBodyShape
    )

    return (
        <div className="container mx-auto py-10">
            <h1 className="text-3xl font-bold mb-6">Detailed Size Chart</h1>
            <div className="flex space-x-4 mb-6">
                <Select onValueChange={(value) => setSelectedGender(value)} defaultValue={selectedGender}>
                    <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Select Gender" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="male">Male</SelectItem>
                        <SelectItem value="female">Female</SelectItem>
                    </SelectContent>
                </Select>
                <Select onValueChange={(value) => setSelectedBodyShape(Number(value))} defaultValue={selectedBodyShape.toString()}>
                    <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Select Body Shape" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="1">Body Shape 1</SelectItem>
                        <SelectItem value="2">Body Shape 2</SelectItem>
                    </SelectContent>
                </Select>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredData.map((cluster) => (
                    <Card key={cluster.cluster_id} className="w-full">
                        <CardHeader>
                            <CardTitle>{cluster.size_label}</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p>Cluster Count: {cluster.cluster_count}</p>
                            <h3 className="font-semibold mt-4 mb-2">Centroid</h3>
                            <ResponsiveContainer width="100%" height={200}>
                                <RadarChart data={[
                                    { name: 'Height', value: cluster.centroid[0] },
                                    { name: 'Weight', value: cluster.centroid[1] },
                                    { name: 'Bust/Chest', value: cluster.centroid[2] },
                                    { name: 'Waist', value: cluster.centroid[3] },
                                    { name: 'Hips', value: cluster.centroid[4] },
                                ]}>
                                    <PolarGrid />
                                    <PolarAngleAxis dataKey="name" />
                                    <PolarRadiusAxis />
                                    <Radar dataKey="value" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                                </RadarChart>
                            </ResponsiveContainer>
                            <h3 className="font-semibold mt-4 mb-2">Sample Data</h3>
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>Height (cm)</TableHead>
                                        <TableHead>Weight</TableHead>
                                        <TableHead>Bust/Chest</TableHead>
                                        <TableHead>Waist</TableHead>
                                        <TableHead>Hips</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {cluster.sample_data.slice(0, 3).map((sample, index) => (
                                        <TableRow key={index}>
                                            <TableCell>{sample.Height_cm}</TableCell>
                                            <TableCell>{sample.Weight}</TableCell>
                                            <TableCell>{sample["Bust/Chest"]}</TableCell>
                                            <TableCell>{sample.Waist}</TableCell>
                                            <TableCell>{sample.Hips}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                            <h3 className="font-semibold mt-4 mb-2">Confidence Scores</h3>
                            <ResponsiveContainer width="100%" height={200}>
                                <BarChart data={Object.entries(cluster.confidence_scores.Height).map(([size, score]) => ({ size, score }))}>
                                    <XAxis dataKey="size" />
                                    <YAxis />
                                    <Tooltip />
                                    <Legend />
                                    <Bar dataKey="score" fill="#8884d8" />
                                </BarChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    )
}