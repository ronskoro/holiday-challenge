"use client";

import SearchForm from "@/app/components/SearchForm/SearchForm";
import {Stack, Typography} from "@mui/material";
import Hotel from "@/app/components/Hotel/Hotel";
import {OpenAPIClientAxios} from "openapi-client-axios";
import {Client, Components, Paths} from "@/app/types/openapi";
import {useEffect, useState} from "react";
import 'text-encoding';
import axios from 'axios';
import Link from "next/link";
import {useRouter, useSearchParams} from "next/navigation";
import BestHotelOffer = Components.Schemas.BestHotelOffer;
import {GetBestOffersByHotelFromQuery, GetBestOffersByHotelToQuery} from "@/app/types/converter";
import { TrySharp } from "@mui/icons-material";

export default function HomePage() {
    const [offers, setOffers] = useState<BestHotelOffer[]>([]);
    const [queryParameters, setQueryParameters] = useState<Paths.GetBestOffersByHotel.QueryParameters>();
    const router = useRouter();
    const query = useSearchParams();

    // update the search form and automatically load offers if a search is existing
    useEffect(() => {
        const parameters = GetBestOffersByHotelFromQuery(query);
        // parameters should be validated here, but as this is a just a very simple implementation we skip this for now
        if(parameters.earliestDepartureDate == null) {
            return;
        }

        load(parameters).catch(console.error);
    }, []);


    async function onSubmitSearchForm(departureAirports: string[], countAdults: number, countChildren: number, duration: number, earliestDeparture: string, latestReturn: string) {
        const parameters: Paths.GetBestOffersByHotel.QueryParameters = {
            earliestDepartureDate: earliestDeparture,
            latestReturnDate: latestReturn,
            countAdults: countAdults,
            countChildren: countChildren,
            departureAirports: departureAirports,
            duration: duration,
        };

        await load(parameters);
    }

    async function load(parameters: Paths.GetBestOffersByHotel.QueryParameters) {
        setQueryParameters(parameters);
        router.push("/?" + GetBestOffersByHotelToQuery(parameters));

        // convert date string to timestamp
        const dateDeparture = new Date(parameters.earliestDepartureDate);
        const earliestDepartureDateString = dateDeparture.toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
          });
        
        const dateReturn = new Date(parameters.latestReturnDate);
        const latestReturnDateString = dateReturn.toLocaleString('en-US', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });

        const date = new Date(earliestDepartureDateString);
        const earliestDepartureDate = date.toISOString().replace('T', ' ').replace('.000Z', '');

        const returnDate = new Date(latestReturnDateString);
        const latestReturnDate = returnDate.toISOString().replace('T', ' ').replace('.000Z', '');

        // console.log(latestReturnDate);

        try {
            const response = await axios.get('http://localhost:5000/search', {
              params: {
                departureAirports: parameters.departureAirports.join(','),
                countAdults: parameters.countAdults,
                countChildren: parameters.countChildren,
                duration: parameters.duration,
                earliestDepartureDate: earliestDepartureDate,
                latestReturnDate: latestReturnDate
              }
            });
        
            setOffers(response.data);
          } catch (error) {
            // Handle the error
            console.error('Error:', error);
          }
        // const api = new OpenAPIClientAxios({definition: 'http://localhost:8090/openapi', withServer: 0})
        // const client = await api.init<Client>()
        // const response = await client.getBestOffersByHotel(parameters);
        // setOffers(response.data);
    }

    return (
        <>
            <Typography sx={{mb: "50px", mt: "40px"}} variant="h3">CHECK24 Holiday Challenge</Typography>
            <SearchForm submitCallback={onSubmitSearchForm}/>
            <Typography variant="h4" sx={{mt: "60px", mb: "30px"}}>Hotels for your Mallorca-Trip:</Typography>
            <Stack gap={3}>
                {offers.map(offer =>
                    <Link key={offer.hotelid}
                          href={{pathname: '/offers', query: {...queryParameters, hotelId: offer.hotelid}}}
                          style={{textDecoration: "none"}}>
                        <Hotel offer={offer}/>
                    </Link>
                )}
            </Stack>
        </>
    )
}