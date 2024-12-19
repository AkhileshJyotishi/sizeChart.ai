'use client'

import { useState } from 'react'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

interface SizeChartItem {
  Size: string
  "Height Range (cm)": string
  "Weight Range (kg)": string
  "Chest/Bust": string
  Waist: string
  Hips: string
}

const sizeChartData: SizeChartItem[] = [
  {
    "Size": "XS",
    "Height Range (cm)": "134.62-150.2",
    "Weight Range (kg)": "40-52",
    "Chest/Bust": `32"-33"`,
    "Waist": `24"-25"`,
    "Hips": `34.5"-35.5"`
  },
  {
    "Size": "S",
    "Height Range (cm)": "150.92-158.26",
    "Weight Range (kg)": "57-74",
    "Chest/Bust": `34"-35"`,
    "Waist": `26"-27"`,
    "Hips": `36"-37"`
  },
  {
    "Size": "M",
    "Height Range (cm)": "151.94-188.82",
    "Weight Range (kg)": "69-77",
    "Chest/Bust": `36"-37"`,
    "Waist": `28"-29"`,
    "Hips": `38.5"-39.5"`
  },
  {
    "Size": "L",
    "Height Range (cm)": "164.4-200.82",
    "Weight Range (kg)": "40-81",
    "Chest/Bust": `38.5"-40"`,
    "Waist": `30.5"-32"`,
    "Hips": `41"-42.5"`
  },
  {
    "Size": "XL",
    "Height Range (cm)": "181.92-210.26",
    "Weight Range (kg)": "40-91",
    "Chest/Bust": `41.5"-43"`,
    "Waist": `33.5"-35"`,
    "Hips": `44"-45.5"`
  }
]

export default function GenericChartPage() {
  const [height, setHeight] = useState('')
  const [weight, setWeight] = useState('')
  const [recommendedSize, setRecommendedSize] = useState('')

  const findSize = () => {
    const heightCm = parseFloat(height)
    const weightKg = parseFloat(weight)

    for (const item of sizeChartData) {
      const [minHeight, maxHeight] = item["Height Range (cm)"].split('-').map(parseFloat)
      const [minWeight, maxWeight] = item["Weight Range (kg)"].split('-').map(parseFloat)

      if (heightCm >= minHeight && heightCm <= maxHeight && weightKg >= minWeight && weightKg <= maxWeight) {
        setRecommendedSize(item.Size)
        return
      }
    }

    setRecommendedSize('No size found')
  }

  return (
    <div className="container mx-auto py-10">
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Generic Size Chart</CardTitle>
          <CardDescription>Find your perfect size based on height and weight</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="space-y-2">
              <Label htmlFor="height">Height (cm)</Label>
              <Input
                id="height"
                placeholder="Enter height in cm"
                value={height}
                onChange={(e) => setHeight(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="weight">Weight (kg)</Label>
              <Input
                id="weight"
                placeholder="Enter weight in kg"
                value={weight}
                onChange={(e) => setWeight(e.target.value)}
              />
            </div>
            <div className="flex items-end">
              <Button onClick={findSize}>Find My Size</Button>
            </div>
          </div>
          {recommendedSize && (
            <div className="text-center p-4 bg-primary/10 rounded-md">
              <p className="text-lg font-semibold">Recommended Size: <span className="text-primary">{recommendedSize}</span></p>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Size Chart</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="font-bold">Size</TableHead>
                  <TableHead className="font-bold">Height Range (cm)</TableHead>
                  <TableHead className="font-bold">Weight Range (kg)</TableHead>
                  <TableHead className="font-bold">Chest/Bust</TableHead>
                  <TableHead className="font-bold">Waist</TableHead>
                  <TableHead className="font-bold">Hips</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sizeChartData.map((item) => (
                  <TableRow key={item.Size} className="hover:bg-muted/50 transition-colors">
                    <TableCell className="font-medium">{item.Size}</TableCell>
                    <TableCell>{item["Height Range (cm)"]}</TableCell>
                    <TableCell>{item["Weight Range (kg)"]}</TableCell>
                    <TableCell>{item["Chest/Bust"]}</TableCell>
                    <TableCell>{item.Waist}</TableCell>
                    <TableCell>{item.Hips}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}