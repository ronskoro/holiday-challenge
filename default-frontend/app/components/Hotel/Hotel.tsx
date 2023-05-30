import {Box, Button, Card, CardMedia, Divider, Rating, Stack, Typography} from "@mui/material";
import {Components} from "@/app/types/openapi";
import BestHotelOffer = Components.Schemas.BestHotelOffer;

interface Properties {
    offer: BestHotelOffer
}

export default function Hotel({offer}: Properties) {
    return (
        <Card variant="outlined" sx={{display: 'flex'}}>
            <Box sx={{backgroundImage: `url("/hotels/${(offer.hotelid % 40) + 1}.jpg")`, width: "355.5px",height: "200px", backgroundSize: "cover"}}/>
            <Box sx={{
                p: 1,
                pl: 2,
                display: 'flex',
                width: '100%',
                flexDirection: 'row',
                justifyContent: 'space-between'
            }}>
                <Stack direction="column" justifyContent="space-between">
                    <Typography sx={{mr: 2}} variant="h6">{offer.hotelname}</Typography>

                    <Stack>
                        <Typography variant="body1">{offer.mealtype !== 'NONE' && offer.mealtype}</Typography>
                        <Typography variant="body1">{offer.roomtype}</Typography>
                    </Stack>

                    <Button variant="contained">View {offer.countAvailableOffers} offers</Button>
                </Stack>
                <Stack direction="column" justifyContent="space-between" alignItems="flex-end">
                    <Rating value={offer.hotelstars} readOnly/>

                    <Stack>
                        <Stack m={0} direction="row" divider={<Divider orientation="vertical" flexItem/>}
                               spacing={1}>
                            <Typography>{offer.duration} Days</Typography>
                            <Typography>{offer.countAdults} Adults</Typography>
                            <Typography>{offer.countChildren} Children</Typography>
                        </Stack>
                        <Typography variant="h6" textAlign="right">from {offer.price} €</Typography>
                    </Stack>
                </Stack>
            </Box>
        </Card>
    );
}