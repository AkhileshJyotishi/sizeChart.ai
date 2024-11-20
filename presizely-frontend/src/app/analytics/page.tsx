'use client'

import { useState } from 'react'
import Image from 'next/image'
import { Card, CardContent } from "@/components/ui/card"
import { Dialog, DialogContent, DialogClose, DialogTitle } from "@/components/ui/dialog"
import { X } from 'lucide-react'
import img1 from "@/app/assets/Untitled.png"
import img2 from "@/app/assets/Untitled2.png"
import img3 from "@/app/assets/girl_Untitled.png"
import img4 from "@/app/assets/girl_Untitled1.png"

export default function GalleryPage() {
    const [selectedImage, setSelectedImage] = useState<any>(null)

    const images = [
        { src: img1, alt: 'male', name: 'male body index 1' },
        { src: img2, alt: 'male2', name: 'male body index 2' },
        { src: img3, alt: 'female', name: 'female body index 1' },
        { src: img4, alt: 'female2', name: 'female body index 2' },
    ]

    return (
        <div className="container mx-auto py-10">
            <h1 className="text-3xl font-bold mb-8">Image Gallery</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {images.map((image) => (
                    <Card key={image.name} className="overflow-hidden cursor-pointer" onClick={() => setSelectedImage(image)}>
                        <CardContent className="p-0">
                            <div className="relative aspect-square">
                                <Image
                                    src={image.src}
                                    alt={image.alt}
                                    fill
                                    className="object-cover transition-transform hover:scale-105"
                                    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                                    priority
                                />
                            </div>
                            <div className="p-4">
                                <p className="text-sm font-medium text-muted-foreground">{image.name}</p>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>


            <Dialog open={selectedImage !== null} onOpenChange={() => setSelectedImage(null)}>
                <DialogContent className="max-w-[90vw] max-h-[90vh] p-0">
                    {/* <VisuallyHidden> */}
                        <DialogTitle>{selectedImage?.alt || 'Full-size image'}</DialogTitle>
                    {/* </VisuallyHidden> */}
                    <DialogClose className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
                        <X className="h-4 w-4" />
                        <span className="sr-only">Close</span>
                    </DialogClose>
                    {selectedImage && (
                        <div className="relative w-full h-full">
                            <Image
                                // @ts-ignore
                                src={selectedImage.src}
                                // @ts-ignore
                                alt={selectedImage.alt}
                                // fill
                                width={800}
                                height={800}
                                className="object-contain w-full"
                                sizes="90vw"
                                priority
                            />
                        </div>
                    )}
                </DialogContent>
            </Dialog>
        </div>
    )
}