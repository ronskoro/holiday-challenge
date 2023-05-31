"use client";

import {OpenAPIClientAxios, Parameters} from "openapi-client-axios";
import {Client, Components, Paths} from "@/app/types/openapi"
import HotelOffer from "@/app/components/HotelOffer/HotelOffer";
import {useSearchParams} from 'next/navigation';
import axios from 'axios';
import {useEffect, useState} from "react";
import {Box, Rating, Typography} from "@mui/material";
import {Stack} from "@mui/system";
import {GetHotelOffersFromQuery} from "@/app/types/converter";
import Hotel from "../components/Hotel/Hotel";

export default function Page() {
    const query = useSearchParams()
    const [hotelOffer, setHotelOffer] = useState<HotelOfferResponse>();

    async function fetchData() {
        const parameters = GetHotelOffersFromQuery(query);

        const earliestDepartureDate = parameters.earliestDepartureDate.replace('T', ' ').replace('.000Z', '');
        const latestReturnDate = parameters.latestReturnDate.replace('T', ' ').replace('.000Z', '');
        
        try {
            const response = await axios.get('http://localhost:5000/offers', {
              params: {
                departureAirports: parameters.departureAirports.join(','),
                countAdults: parameters.countAdults,
                countChildren: parameters.countChildren,
                duration: parameters.duration,
                earliestDepartureDate: earliestDepartureDate,
                latestReturnDate: latestReturnDate,
                hotelid: parameters.hotelId
              }
            });
        
            setHotelOffer(response.data);
          } catch (error) {
            // Handle the error
            console.error('Error:', error);
          }
        // const api = new OpenAPIClientAxios({definition: 'http://localhost:8090/openapi', withServer: 0})
        // const client = await api.init<Client>()
        // const response = await client.GetHotelOffers(parameters)
        // setHotelOffer(response.data);   
    }

    useEffect(() => {
        fetchData().catch(console.error);
    }, []);

    if (hotelOffer == null) {
        return <p>Loading offers...</p>
    }

    return (
        <>
            <Stack direction="row" pt={5} alignItems="center">
                <Typography variant="h4" mr={2}>{hotelOffer[0].hotelname}</Typography>
                <Rating value={hotelOffer[0].hotelstars} readOnly/>
            </Stack>
            <Stack direction="row" height="250px" pt={2}>
                <Box sx={{borderTopLeftRadius: "5px", borderBottomLeftRadius: "5px", backgroundImage: `url("/hotels/${(hotelOffer[0].hotelid % 40) + 1}.jpg")`, width: "50%", backgroundSize: "cover", backgroundPosition: "center"}}/>
                <Box sx={{borderTopRightRadius: "5px", borderBottomRightRadius: "5px", backgroundImage: `url("/rooms/${(hotelOffer[0].hotelid % 30) + 1}.jpg")`, width: "50%", backgroundSize: "cover", backgroundPosition: "center"}}/>
            </Stack>
            <Typography pt={2} variant="h6">Offers:</Typography>
            <Stack gap={2} mt={1}>
                {hotelOffer.map((offer: Components.Schemas.Offer) =>
                    <HotelOffer key={offer.price} offer={offer}/>
                )}
            </Stack>
        </>
    )
}